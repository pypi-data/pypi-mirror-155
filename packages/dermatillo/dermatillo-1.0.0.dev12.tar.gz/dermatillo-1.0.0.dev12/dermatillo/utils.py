import datetime
import os
import sys
import time
import json
import uuid
import psutil
import datetime
import threading
import numpy as np
import sounddevice as sd
from filelock import FileLock
from dermatillo.config import *
from dermatillo.platforms import platform

DERMATILLO_DIR = os.path.dirname(os.path.realpath(__file__))


class UnpredictedException(Exception):
    def __init__(self, exception: Exception):
        os.makedirs(platform.data_dir, exist_ok=True)
        log_path = os.path.join(platform.data_dir, "dermatillo.log")
        with FileLock(f"{log_path}.lock").acquire(timeout=10):
            with open(log_path, "a") as file:
                file.write(f"{datetime.datetime.now()} - {type(exception).__name__} occurred\n")
        raise exception


class Timer:
    def __init__(self, period_sec: float):
        self.__period_sec = period_sec
        self.__start = time.time()

    def wait(self):
        wait_time = self.__period_sec - (time.time() - self.__start)
        time.sleep(max(wait_time, 0.))
        self.__start = time.time()


class BackEndDispatcher:
    def __init__(self, back_end, back_end_init_args: dict, back_ends_per_source: int, back_ends_per_source_max: int):
        self.__back_end = back_end
        self.__back_end_init_args = back_end_init_args

        if os.environ.get("DERMATILLO_SETUP") == "1":
            self.__back_ends_count = 1 * back_ends_per_source
            self.__back_ends_limit = 1 * back_ends_per_source_max
        else:
            self.__back_ends_count = VIDEO_SOURCES_COUNT * back_ends_per_source
            self.__back_ends_limit = VIDEO_SOURCES_COUNT * back_ends_per_source_max
        self.__back_ends_pool = [back_end(**back_end_init_args) for _ in range(self.__back_ends_count)]

        self.__active_back_ends_count = len(self.__back_ends_pool)
        self.__lock = threading.Lock()

    class BackEndLimitReached(Exception):
        def __init__(self, back_ends_limit: int):
            super().__init__(f"({back_ends_limit})")

    def __get_back_end(self):
        self.__lock.acquire()
        if len(self.__back_ends_pool) > 0:
            back_end = self.__back_ends_pool.pop(0)
            self.__lock.release()
            return back_end
        elif self.__active_back_ends_count < self.__back_ends_limit:
            self.__active_back_ends_count += 1
            self.__lock.release()
            return self.__back_end(**self.__back_end_init_args)
        else:
            self.__lock.release()
            raise self.BackEndLimitReached(self.__back_ends_limit)

    def __return_back_end(self, back_end):
        self.__lock.acquire()
        if self.__active_back_ends_count > self.__back_ends_count:
            del back_end
        else:
            self.__back_ends_pool.append(back_end)
        self.__active_back_ends_count -= 1
        self.__lock.release()

    def run(self, input_array: np.array):
        back_end = self.__get_back_end()
        output = back_end.process(input_array)
        self.__return_back_end(back_end)
        return output


class MissionControl(threading.Thread):
    def __init__(self):
        super().__init__(name=f"{self.__class__.__name__} - {uuid.uuid4()}", daemon=True)
        self._file_path = "/tmp/dermatillo_process.json"
        self._file_lock = FileLock(f"{self._file_path}.lock")
        self.is_halted = False

    def _load(self):
        self._file_lock.acquire()
        try:
            with open(self._file_path, "r") as file:
                meta_data = json.load(file)
        finally:
            self._file_lock.release()
        return meta_data

    def run(self):
        while True:
            meta_data = self._load()
            self.is_halted = time.time() - meta_data["halted_at"] < meta_data["halted_for"] * 60
            time.sleep(0.5)

    def attempt_register(self):
        if os.path.exists(self._file_path):
            if psutil.pid_exists(self._load()["pid"]):
                print("Dermatillo is already running on the system.")
                sys.exit(1)

        meta_data = {"pid": os.getpid(), "start": time.time(), "halted_at": 0., "halted_for": 0}
        self._file_lock.acquire()
        try:
            with open(self._file_path, "w") as file:
                json.dump(meta_data, file)
        finally:
            self._file_lock.release()

    def halt(self, time_out):
        meta_data = self._load()
        self._file_lock.acquire()
        try:
            meta_data["halted_at"] = time.time()
            meta_data["halted_for"] = time_out
            with open(self._file_path, "w") as file:
                json.dump(meta_data, file)
        finally:
            self._file_lock.release()


class Alarm(threading.Thread):
    def __init__(self, audio_output_device):
        super().__init__(name=f"{self.__class__.__name__} - {uuid.uuid4()}", daemon=True)
        self._triggered_at = 0.
        if os.environ.get("DERMATILLO_SETUP") == "1":
            self._amplitude = 0.2
            self._frequency = 5000
            self._alarm_sound_duration = 3
        else:
            self._amplitude = ALARM_SOUND_AMPLITUDE
            self._frequency = ALARM_SOUND_FREQUENCY
            self._alarm_sound_duration = ALARM_SOUND_DURATION_SEC
        self._start_idx = 0
        for i, device in enumerate(sd.query_devices()):
            crop_idx = device["name"].find("(hw:")
            if crop_idx == -1:
                name = device["name"]
            else:
                name = device["name"][:crop_idx]
            if name == audio_output_device:
                self._sample_rate = device["default_samplerate"]
                self._output_stream = sd.OutputStream(
                    device=i,
                    samplerate=self._sample_rate,
                    channels=device["max_output_channels"],
                    callback=self._sine_wave
                )
                break
        else:
            raise self.AudioDeviceNotFound(audio_output_device)

    class AudioDeviceNotFound(Exception):
        def __init__(self, audio_output_device: str):
            super().__init__(f"'{audio_output_device}'")

    def _sine_wave(self, outdata, frames, _, __):
        t = (self._start_idx + np.arange(frames)) / self._sample_rate
        t = t.reshape(-1, 1)
        outdata[:] = self._amplitude * np.sin(2 * np.pi * self._frequency * t)
        self._start_idx += frames

    def trigger(self):
        self._triggered_at = time.time()

    def run(self):
        while True:
            time_passed = time.time() - self._triggered_at
            if time_passed < self._alarm_sound_duration:
                if not self._output_stream.active:
                    self._output_stream.start()
                time.sleep(self._alarm_sound_duration - time_passed)
            elif self._output_stream.active:
                self._output_stream.stop()
            time.sleep(0.1)


mission_control = MissionControl()
if os.environ.get("DERMATILLO_SETUP") != "1":
    mission_control.attempt_register()
    mission_control.start()
    alarm = Alarm(AUDIO_OUTPUT_DEVICE)
    alarm.start()
