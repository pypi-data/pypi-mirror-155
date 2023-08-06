import time
import uuid
from threading import Thread
from dermatillo.people_tracking import PeopleTracker
from dermatillo.face_detection import FaceDetector
from dermatillo.features_extraction import FeaturesExtractor
from dermatillo.video_capture import VideoCapture
from dermatillo.behavior_classification import BehaviorClassifier
from typing import Union
from dermatillo.utils import Timer
from dermatillo.config import *


class VideoCaptureObserver(Thread):
    def __init__(self, video_source_id: Union[int, str]):
        super().__init__(name=f"{self.__class__.__name__} - {uuid.uuid4()}", daemon=True)
        self.unpredicted_exception = None
        self.__video_capture = VideoCapture(video_source_id)
        self.__people_tracker = PeopleTracker()
        self.__face_detector = FaceDetector(self.__video_capture, self.__people_tracker)
        self.__features_extractor = FeaturesExtractor(self.__video_capture, self.__people_tracker)
        self.__behavior_classifier = BehaviorClassifier(self.__people_tracker)

    def run(self):
        try:
            while True:
                self.__check()
                time.sleep(FACE_DETECTION_PERIOD_SEC)
        except Exception as exception:
            self.unpredicted_exception = exception

    def __check(self):
        def stop_all():
            self.__features_extractor.stop()
            self.__face_detector.stop()
            self.__video_capture.stop()

        try:
            self.__video_capture.start()
        except (self.__video_capture.NotAvailable, self.__video_capture.TimeOutExceeded):
            return
        try:
            self.__behavior_classifier.reset()
            self.__face_detector.start()
            self.__features_extractor.start()
            timer = Timer(BEHAVIOR_CLASSIFICATION_PERIOD_SEC)
            while self.__face_detector.is_alive() and self.__features_extractor.is_alive():
                self.__behavior_classifier.check()
                timer.wait()
            stop_all()
        except Exception as exception:
            stop_all()
            raise exception
