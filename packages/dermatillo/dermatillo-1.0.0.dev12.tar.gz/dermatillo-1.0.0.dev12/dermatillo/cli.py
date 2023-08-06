import os
import cv2
import sys
import json
import time
import click
import sounddevice as sd
from filelock import FileLock
from dermatillo.platforms import get_platform

dermatillo_dir = os.path.dirname(os.path.realpath(__file__))
platform = get_platform()


def get_choice(options: list[str]) -> str:
    answer = None
    while answer not in options:
        answer = input(f"\033[93m{' | '.join(options)} (type in)\n\033[0m")
    return answer


def get_boolean_answer(question: str) -> bool:
    answer = None
    while answer not in ["y", "n"]:
        answer = input(f"\033[93m{question} (y/n)\033[0m")
    return answer == "y"


def select_item(prompt: str, iterable: iter):
    while True:
        try:
            return iterable[int(input(f"\033[93m{prompt}\033[0m"))]
        except (ValueError, IndexError):
            continue


class Config:
    def __init__(self) -> None:
        if os.path.exists(platform.config_file_path):
            config_path = platform.config_file_path
        else:
            config_path = os.path.join(dermatillo_dir, "files/config.json")

        with open(config_path, "r") as file:
            self.dict = json.load(file)

    def save(self) -> None:
        os.makedirs(platform.config_file_dir, exist_ok=True)
        with open(platform.config_file_path, "w") as file:
            json.dump(self.dict, file)


class NaturalOrderGroup(click.Group):
    def list_commands(self, ctx):
        return self.commands.keys()


@click.group(cls=NaturalOrderGroup)
def entry() -> None:
    pass


class VideoSources:
    def __init__(self) -> None:
        self._display_window_height = 500
        self._display_window_offset = 150
        self._display_frame_rate = 60
        self._display_duration_sec = 3
        self._selected_sources = []

    def _query_user(self, source_id: str) -> None:
        if source_id in self._selected_sources:
            print(f"\n\033[91m{source_id} is already selected!\033[0m")
            return

        os.environ["DERMATILLO_SETUP"] = "1"
        from dermatillo.video_capture import VideoCapture

        video_capture = VideoCapture(source_id)
        try:
            video_capture.start(time_out=3)
        except (video_capture.NotAvailable, video_capture.TimeOutExceeded):
            print(f"\n\033[91m{source_id} is not available\033[0m")
            return

        choice = None
        while choice not in ["add", "skip"]:
            print(f"\n{source_id}")
            choice = get_choice(["add", "test", "skip"])
            if choice == "add":
                self._selected_sources.append(source_id)
                print(f"\033[92m{source_id} added\033[0m")
            elif choice == "test":
                print("displaying camera image ...")
                shape = video_capture.get_frame().data.shape
                ratio = self._display_window_height / shape[0]
                target_size = (int(shape[1] * ratio), int(shape[0] * ratio))
                cv2.namedWindow(source_id)
                cv2.moveWindow(source_id, self._display_window_offset, self._display_window_offset)
                start = time.time()
                while time.time() - start < self._display_duration_sec:
                    bgr_frame = cv2.cvtColor(video_capture.get_frame().data, cv2.COLOR_RGB2BGR)
                    cv2.imshow(source_id, cv2.resize(bgr_frame, dsize=target_size))
                    _ = cv2.waitKey(int(1000 / self._display_frame_rate))
                cv2.destroyAllWindows()
        video_capture.stop()

    def get(self) -> list[str]:
        v4l_dir = "/dev/v4l/by-path"
        if platform.name == "Linux" and os.path.exists(v4l_dir):
            physical_video_sources = sorted(os.listdir(v4l_dir))
            for source_id in physical_video_sources:
                self._query_user(os.path.join(v4l_dir, source_id))
        elif get_boolean_answer("\nDo you want Dermatillo to use physically connected cameras?"):
            self._selected_sources.append("ALL_CONNECTED")

        add_network_source = get_boolean_answer("\nDo you want to add network camera?")
        while add_network_source:
            self._query_user(input("\033[93m  Please input IP address:\n  \033[0m"))
            add_network_source = get_boolean_answer("\nDo you want to add another network camera?")

        if len(self._selected_sources) == 0:
            print(f"\n\033[91mPlease select at least one video source!\033[0m")
            return self.get()
        return self._selected_sources


class AudioOutput:
    def __init__(self) -> None:
        pass

    def _query_user(self) -> str:
        available_audio_output = []
        print("\nAvailable audio output devices:")
        n = 0
        for device in sd.query_devices():
            if device["max_output_channels"] > 0:
                crop_idx = device["name"].find("(hw:")
                if crop_idx == -1:
                    name = device["name"]
                else:
                    name = device["name"][:crop_idx]
                available_audio_output.append(name)
                if name == "default":
                    print(f"  {n}: {name}  <--- recommended")
                else:
                    print(f"  {n}: {name}")
                n += 1
        print()
        return select_item("Please input index of selected audio output device: ", available_audio_output)

    def get(self) -> str:
        os.environ["DERMATILLO_SETUP"] = "1"
        from dermatillo.utils import Alarm

        audio_output = self._query_user()
        choice = None
        while choice not in ["add"]:
            print(f"\n{audio_output}")
            choice = get_choice(["add", "test", "change"])
            if choice == "test":
                alarm = Alarm(audio_output)
                alarm.start()
                print("playing alarm signal ...")
                alarm.trigger()
            elif choice == "change":
                audio_output = self._query_user()

        return audio_output


@click.command()
def set_up() -> None:
    def confirm_config(prompt: str) -> None:
        video_sources = configuration.dict["VIDEO_SOURCES"]
        audio_output_device = configuration.dict["AUDIO_OUTPUT_DEVICE"]
        if len(video_sources) > 0:
            print("\nvideo sources:")
            for i, video_source_id in enumerate(video_sources):
                print(f"  {i}: {video_source_id}")
            print(f"\naudio output device:\n  {audio_output_device}")
            if get_boolean_answer(prompt) is False:
                sys.exit(0)

    configuration = Config()
    confirm_config("\nDo you want to overwrite current I/O set-up?")

    # stop service if it's existing to release video sources and not mangle with config in general
    service_stopped = platform.stop_service()

    configuration.dict["VIDEO_SOURCES"] = VideoSources().get()
    configuration.dict["AUDIO_OUTPUT_DEVICE"] = AudioOutput().get()
    confirm_config("\nDo you want to continue with this I/O set-up?")
    configuration.save()

    if service_stopped:
        platform.start_service()
    elif get_boolean_answer("\nDo you want to set Dermatillo as a service?"):
        platform.set_service()

    print("\n\033[92mConfiguration completed.\033[0m")


@click.command()
def service_status() -> None:
    platform.service_active()


@click.command()
def service_remove() -> None:
    platform.remove_service()


@click.command()
def run() -> None:
    from dermatillo.run import entry
    entry()


@click.command()
def halt() -> None:
    time_out = None
    while time_out is None:
        try:
            time_out = int(input("\033[93mPlease input minutes: \033[0m"))
        except (TypeError, ValueError):
            continue
    if time_out > 720 and not get_boolean_answer(f"Are you sure you want to halt Dermatillo for {time_out} minutes?"):
        sys.exit(0)
    os.environ["DERMATILLO_SETUP"] = "1"
    from dermatillo.utils import mission_control
    mission_control.halt(time_out)


@click.command()
def stats():
    pass


@click.command()
def enable_data_collection():
    pass


@click.command()
def disable_data_collection():
    pass


@click.command()
def log():
    log_path = os.path.join(platform.data_dir, "dermatillo.log")
    if os.path.exists(log_path):
        with FileLock(f"{log_path}.lock").acquire(timeout=1):
            with open(log_path, "r") as file:
                log_content = file.readlines()
        input(f"Latest status: {log_content[-1]}")
        print(f"\nFull log available under {log_path}")
    else:
        print("No logs found.")


@click.command()
def alarm_settings() -> None:
    alarm_parameters = [
        "ALARM_SOUND_AMPLITUDE",
        "ALARM_SOUND_FREQUENCY",
        "ALARM_SOUND_DURATION_SEC",
        "ALARM_ACTIVATION_THRESHOLD",
        "ALARM_ACTIVATION_STRIKE"
    ]

    os.environ["DERMATILLO_SETUP"] = "1"
    from dermatillo.config import cast_value
    config = Config()

    print("Current settings:")
    for parameter in alarm_parameters:
        print(f"  {parameter}: {config.dict[parameter]}")

    if get_boolean_answer("\nDo you want to modify parameters listed above?"):
        parameter = input("Please input name of parameter to be changed: ")
        while parameter not in alarm_parameters:
            print(f"Choices: {alarm_parameters}")
            parameter = input("Please input name of parameter to be changed: ")
        value = None
        while value is None:
            value = cast_value(parameter, input("Please input new value: "))
        config.dict[parameter] = value
        config.save()


@click.command()
def benchmark() -> None:
    os.environ["DERMATILLO_SETUP"] = "1"
    from dermatillo.benchmark import run
    run()


@click.command()
def version() -> None:
    import dermatillo
    print(f"{dermatillo.__name__}-{dermatillo.__version__}")


@click.command()
def legal() -> None:
    print("\nCopyright (c) 2022 by Jan Grzybek, lyre_embassy_0n@icloud.com")
    print("All Rights Reserved.\n")
    input("Press ENTER to print out LICENSE text")
    print()
    with open(os.path.join(dermatillo_dir, "files/LICENSE"), "r") as f:
        print(f.read())


entry.add_command(set_up)
entry.add_command(service_status)
entry.add_command(service_remove)
entry.add_command(run)
entry.add_command(halt)
entry.add_command(stats)
entry.add_command(enable_data_collection)
entry.add_command(disable_data_collection)
entry.add_command(log)
entry.add_command(alarm_settings)
entry.add_command(benchmark)
entry.add_command(version)
entry.add_command(legal)
