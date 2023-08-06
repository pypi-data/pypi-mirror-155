import sys
import time
from dermatillo.config import *


def check_config():
    if sys.platform not in ["linux", "darwin"]:
        print("\n\033[91mDermatillo is available only on Unix.\033[0m")
        sys.exit(0)

    if AUDIO_OUTPUT_DEVICE == "" or VIDEO_SOURCES_COUNT == 0:
        report_missing_config()


class ObserverDead(Exception):
    pass


def entry():
    check_config()
    from dermatillo.observation import VideoCaptureObserver

    active_observers = []
    for video_source_id in VIDEO_SOURCE_IDS:
        observer = VideoCaptureObserver(video_source_id)
        observer.start()
        active_observers.append(observer)

    print("Started monitoring of following video sources:")
    for video_source_id in VIDEO_SOURCE_IDS:
        print(f"  {video_source_id}")

    while True:
        for observer in active_observers:
            if observer.unpredicted_exception:
                raise observer.unpredicted_exception
            if not observer.is_alive():
                raise ObserverDead
        time.sleep(1)


if __name__ == "__main__":
    entry()
