import os
import cv2
import sys
import json


def find_local_video_devices():
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
    return available_ids


def report_missing_config():
    print("First, please complete configuration by running 'dermatillo config' command.")
    sys.exit(0)


try:
    with open(os.path.join(os.path.expanduser("~"), ".config/dermatillo/config.json"), "r") as f:
        config = json.load(f)
except FileNotFoundError:
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "files/config.json"), "r") as f:
        config = json.load(f)

TIME_SERIES_SECONDS = config["TIME_SERIES_SECONDS"]
TIME_SERIES_POINTS_PER_SEC = config["TIME_SERIES_POINTS_PER_SEC"]
assert type(TIME_SERIES_POINTS_PER_SEC) is int
_TIME_SERIES_POINTS_COUNT = TIME_SERIES_SECONDS * TIME_SERIES_POINTS_PER_SEC
TIME_SERIES_POINTS_COUNT = int(_TIME_SERIES_POINTS_COUNT)
assert _TIME_SERIES_POINTS_COUNT % TIME_SERIES_POINTS_COUNT == 0

BEHAVIOR_CLASSIFICATION_PERIOD_SEC = config["BEHAVIOR_CLASSIFICATION_PERIOD_SEC"]

FACE_DETECTION_FRAMES_PER_SEC = config["FACE_DETECTION_FRAMES_PER_SEC"]
BBOX_FACE_THRESHOLD = config["BBOX_FACE_THRESHOLD"]

FEATURES_EXTRACTION_FRAMES_PER_SEC = config["FEATURES_EXTRACTION_FRAMES_PER_SEC"]

STANDARD_CHECK_PERIOD_SEC = config["STANDARD_CHECK_PERIOD_SEC"]
FREQUENT_CHECK_PERIOD_SEC = config["FREQUENT_CHECK_PERIOD_SEC"]

PERSON_TRACKING_TIME_OUT_SEC = config["PERSON_TRACKING_TIME_OUT_SEC"]

ALARM_SOUND_AMPLITUDE = config["ALARM_SOUND_AMPLITUDE"]
ALARM_SOUND_FREQUENCY = config["ALARM_SOUND_FREQUENCY"]
ALARM_SOUND_DURATION = config["ALARM_SOUND_DURATION"]

ALARM_ACTIVATION_THRESHOLD = config["ALARM_ACTIVATION_THRESHOLD"]
ALARM_DEACTIVATION_THRESHOLD = config["ALARM_DEACTIVATION_THRESHOLD"]
ALARM_ACTIVATION_STRIKE = config["ALARM_ACTIVATION_STRIKE"]
ALARM_DEACTIVATION_STRIKE = config["ALARM_DEACTIVATION_STRIKE"]
INCREASED_ALERT_TIME_OUT = config["INCREASED_ALERT_TIME_OUT"]

AUDIO_OUTPUT_DEVICE = config["AUDIO_OUTPUT_DEVICE"]
VIDEO_SOURCE_IDS = config["VIDEO_SOURCES"]
if sys.platform != "linux":
    VIDEO_SOURCE_IDS += find_local_video_devices()
VIDEO_SOURCES_COUNT = len(VIDEO_SOURCE_IDS)

del config
