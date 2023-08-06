import cv2
import uuid
import time
from threading import Thread
from dermatillo.objects import Frame
from typing import Union
from dermatillo.utils import UnpredictedException, mission_control


class VideoCaptureIssue(Exception):
    # TO-DO LOG FAILURE
    pass


class FrameReader(Thread):
    def __init__(self, source_id: Union[int, str]):
        super().__init__(name=f"{self.__class__.__name__} - {uuid.uuid4()}", daemon=True)
        self.__unpredicted_exception = None
        self.success = None
        self.capture_opened = None
        self.frame = None
        self.__do_read = True
        self.__source_id = source_id

    def run(self):
        try:
            capture = cv2.VideoCapture(self.__source_id)
            self.capture_opened = capture.isOpened()

            if self.capture_opened:
                while self.__do_read:
                    is_success, frame = capture.read()
                    if is_success and not mission_control.is_halted:
                        self.frame = Frame(time.time(), cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                        self.success = True
                    else:
                        self.frame = None
                        break
            else:
                # TO-DO: general log maintainer > info about unsuccessful capture opening
                pass

            capture.release()
            self.success = False
        except Exception as exception:
            self.__unpredicted_exception = exception

    def is_active(self):
        return self.is_alive() and self.capture_opened

    def stop(self):
        self.__do_read = False
        self.join()
        if self.__unpredicted_exception is not None:
            raise UnpredictedException(self.__unpredicted_exception)


class VideoCapture:
    def __init__(self, source_id: Union[int, str]):
        self.__source_id = source_id
        self.__reader = None

    class EmptyFrame(Exception):
        pass

    class NotAvailable(Exception):
        pass

    class TimeOutExceeded(Exception):
        def __init__(self, time_out: float):
            super().__init__(f"({time_out} seconds)")

    def start(self, time_out: float = 10.):
        if mission_control.is_halted:
            raise self.NotAvailable

        self.stop()

        assert self.__reader is None
        self.__reader = FrameReader(self.__source_id)
        self.__reader.start()

        while self.__reader.capture_opened is None:
            time.sleep(0.001)

        if not self.__reader.is_active():
            self.stop()
            raise self.NotAvailable

        start = time.time()
        while self.__reader.success is None and time.time() - start < time_out:
            time.sleep(0.001)
        if self.__reader.success is not True:
            self.stop()
            raise self.TimeOutExceeded(time_out)

    def stop(self):
        if self.__reader is not None:
            self.__reader.stop()
            self.__reader = None

    def get_frame(self) -> Frame:
        if self.__reader is None or not self.__reader.is_active():
            self.stop()
            raise self.NotAvailable
        else:
            if self.__reader.frame is None:
                self.stop()
                raise self.EmptyFrame
            else:
                return self.__reader.frame
