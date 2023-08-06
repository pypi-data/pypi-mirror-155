import os
import cv2
import sys
import json
from dermatillo.platforms import get_platform
from typing import Union


def cast_value(parameter: str, value: str) -> Union[None, int, float]:
    if parameter in ["ALARM_SOUND_AMPLITUDE", "ALARM_SOUND_DURATION_SEC"]:
        try:
            value = float(value)
            if value > 0.:
                return value
        except ValueError:
            pass
        print("\033[91mValue must be a non-zero positive float\033[0m")
    elif parameter in ["ALARM_SOUND_FREQUENCY", "ALARM_ACTIVATION_STRIKE"]:
        try:
            value = float(value)
            if value > 0 and value % 1 == 0:
                return int(value)
        except ValueError:
            pass
        print("\033[91mValue must be a non-zero positive integer\033[0m")
    elif parameter == "ALARM_ACTIVATION_THRESHOLD":
        try:
            value = float(value)
            if 1.0 >= value >= 0.:
                return value
        except ValueError:
            pass
        print("\033[91mValue must be a positive float in 0. <> 1.0 range\033[0m")
    else:
        raise ValueError(f"Parameter {parameter} is not handled")

    return None


def find_physical_video_devices() -> list[int]:
    source_id = 0
    unavailable_ids = []
    available_ids = []
    while not len(unavailable_ids) >= 5:
        is_success = False
        video_capture = cv2.VideoCapture(source_id)
        if video_capture.isOpened():
            is_success, _ = video_capture.read()
            if is_success:
                available_ids.append(source_id)
        if not is_success:
            unavailable_ids.append(source_id)
        source_id += 1
    if len(available_ids) == 0:
        print("\033[91mCouldn't find any physically connected camera!\033[0m")
        sys.exit(1)
    return available_ids


if os.environ.get("DERMATILLO_SETUP") != "1":
    platform = get_platform()
    try:
        with open(platform.config_file_path, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("First, please complete configuration by running 'dermatillo set-up' command.")
        sys.exit(0)

    TIME_SERIES_SECONDS = config["TIME_SERIES_SECONDS"]
    TIME_SERIES_POINTS_PER_SEC = config["TIME_SERIES_POINTS_PER_SEC"]
    assert type(TIME_SERIES_POINTS_PER_SEC) is int
    _TIME_SERIES_POINTS_COUNT = TIME_SERIES_SECONDS * TIME_SERIES_POINTS_PER_SEC
    TIME_SERIES_POINTS_COUNT = int(_TIME_SERIES_POINTS_COUNT)
    assert _TIME_SERIES_POINTS_COUNT % TIME_SERIES_POINTS_COUNT == 0

    BEHAVIOR_CLASSIFICATION_PERIOD_SEC = config["BEHAVIOR_CLASSIFICATION_PERIOD_SEC"]

    FACE_DETECTION_PERIOD_SEC = config["FACE_DETECTION_PERIOD_SEC"]
    FACE_DETECTION_FRAMES_PER_SEC = config["FACE_DETECTION_FRAMES_PER_SEC"]
    BBOX_FACE_THRESHOLD = config["BBOX_FACE_THRESHOLD"]

    FEATURES_EXTRACTION_FRAMES_PER_SEC = config["FEATURES_EXTRACTION_FRAMES_PER_SEC"]

    PERSON_TRACKING_TIME_OUT_SEC = config["PERSON_TRACKING_TIME_OUT_SEC"]

    ALARM_SOUND_AMPLITUDE = config["ALARM_SOUND_AMPLITUDE"]
    ALARM_SOUND_FREQUENCY = config["ALARM_SOUND_FREQUENCY"]
    ALARM_SOUND_DURATION_SEC = config["ALARM_SOUND_DURATION_SEC"]

    ALARM_ACTIVATION_THRESHOLD = config["ALARM_ACTIVATION_THRESHOLD"]
    ALARM_ACTIVATION_STRIKE = config["ALARM_ACTIVATION_STRIKE"]

    AUDIO_OUTPUT_DEVICE = config["AUDIO_OUTPUT_DEVICE"]
    VIDEO_SOURCE_IDS = config["VIDEO_SOURCES"]
    if "ALL_CONNECTED" in config["VIDEO_SOURCES"]:
        VIDEO_SOURCE_IDS += find_physical_video_devices()
    VIDEO_SOURCES_COUNT = len(VIDEO_SOURCE_IDS)

    del config
