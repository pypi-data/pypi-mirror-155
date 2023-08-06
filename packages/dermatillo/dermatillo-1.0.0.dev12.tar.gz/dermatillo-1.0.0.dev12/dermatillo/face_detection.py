import mediapipe as mp
from dermatillo.utils import BackEndDispatcher
from dermatillo.video_capture import VideoCapture, VideoCaptureIssue
from dermatillo.people_tracking import PeopleTracker
from threading import Thread
from dermatillo.utils import Timer, UnpredictedException
import uuid
from dermatillo.objects import BBox, Frame
from dermatillo.config import *

face_detector_back_end = BackEndDispatcher(
    mp.solutions.face_detection.FaceDetection,
    {"model_selection": 1, "min_detection_confidence": BBOX_FACE_THRESHOLD},
    back_ends_per_source=1,
    back_ends_per_source_max=1
)


class FaceDetector:
    def __init__(self, video_capture: VideoCapture, people_tracker: PeopleTracker):
        self._thread = None
        self.__unpredicted_exception = None
        self.__do_track = None
        self.__video_capture = video_capture
        self.__people_tracker = people_tracker

    def __detect_faces(self, frame: Frame):
        output = face_detector_back_end.run(frame.data)

        if output.detections:
            bboxes = []

            for detection in output.detections:
                rel_bbox = detection.location_data.relative_bounding_box

                side_padding = rel_bbox.width
                top_padding = 1.5 * rel_bbox.height
                bottom_padding = rel_bbox.height

                # x,y coordinates here have their origin point in the top-left corner of the input image, therefore
                # y_min is a top of a bbox, and we subtract top_padding from it
                x_min = rel_bbox.xmin - side_padding
                x_max = rel_bbox.xmin + rel_bbox.width + side_padding
                y_min = rel_bbox.ymin - top_padding
                y_max = rel_bbox.ymin + rel_bbox.height + bottom_padding

                x_min = max(0., x_min)
                x_max = min(1.0, x_max)
                y_min = max(0., y_min)
                y_max = min(1.0, y_max)

                bboxes.append(BBox(x_min, x_max, y_min, y_max))

            self.__people_tracker.process_bboxes(frame.capture_time, bboxes)

    def _run(self):
        def process_frame():
            try:
                self.__detect_faces(self.__video_capture.get_frame())
            except (self.__video_capture.NotAvailable, self.__video_capture.EmptyFrame):
                raise VideoCaptureIssue
            timer.wait()

        try:
            self.__do_track = True
            timer = Timer(1 / FACE_DETECTION_FRAMES_PER_SEC)
            try:
                process_frame()
                while self.__do_track and len(self.__people_tracker.get()) > 0:
                    process_frame()
            except VideoCaptureIssue:
                return
        except Exception as exception:
            self.__unpredicted_exception = exception

    def is_alive(self):
        return self._thread.is_alive()

    def start(self):
        assert self._thread is None or not self._thread.is_alive()
        self._thread = Thread(target=self._run, name=f"{self.__class__.__name__} - {uuid.uuid4()}", daemon=True)
        self._thread.start()

    def stop(self):
        self.__do_track = False
        self._thread.join()
        if self.__unpredicted_exception is not None:
            raise UnpredictedException(self.__unpredicted_exception)
