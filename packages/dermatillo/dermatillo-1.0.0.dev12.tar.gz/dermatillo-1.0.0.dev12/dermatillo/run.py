import time
from dermatillo.config import *
from dermatillo.utils import UnpredictedException


class ObserverDead(Exception):
    pass


def entry():
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
                raise UnpredictedException(observer.unpredicted_exception)
            if not observer.is_alive():
                raise UnpredictedException(ObserverDead())
        time.sleep(1)


if __name__ == "__main__":
    entry()
