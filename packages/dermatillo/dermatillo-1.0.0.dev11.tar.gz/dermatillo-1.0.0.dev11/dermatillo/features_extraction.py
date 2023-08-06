import uuid
import numpy as np
import mediapipe as mp
from threading import Thread
from dermatillo.video_capture import VideoCapture
from dermatillo.people_tracking import PeopleTracker
from dermatillo.utils import Timer, BackEndDispatcher, UnpredictedException
from dermatillo.objects import Frame, Person
from dermatillo.config import *


face_features_back_end = BackEndDispatcher(
    mp.solutions.face_mesh.FaceMesh,
    {
        "refine_landmarks": True,
        "min_detection_confidence": 0.5,
        "min_tracking_confidence": 0.5,
        "max_num_faces": 1,
        "static_image_mode": False
    },
    back_ends_per_source=3,
    back_ends_per_source_max=10
)

hand_features_back_end = BackEndDispatcher(
    mp.solutions.hands.Hands,
    {
        "model_complexity": 1,
        "min_detection_confidence": 0.5,
        "min_tracking_confidence": 0.5,
        "max_num_hands": 2,
        "static_image_mode": False
    },
    back_ends_per_source=3,
    back_ends_per_source_max=10
)


class FeaturesExtractor:
    def __init__(self, video_capture: VideoCapture, people_tracker: PeopleTracker):
        self._thread = None
        self.__unpredicted_exception = None
        self.__do_process = None
        self.__video_capture = video_capture
        self.__people_tracker = people_tracker

    def _extract_hands_data(self, person: Person, frame: Frame):
        try:
            output = hand_features_back_end.run(frame.data)
            if output.multi_hand_landmarks:
                hand_scores = {"Left": -1.0, "Right": -1.0}
                hand_idx = {"Left": None, "Right": None}
                subarray = np.full((2*person.features.hand_landmarks_count, person.features.dims), -1.0)

                for i, detection in enumerate(output.multi_handedness):
                    hand_data = detection.classification[0]
                    if hand_data.score > hand_scores[hand_data.label]:
                        hand_scores[hand_data.label] = hand_data.score
                        hand_idx[hand_data.label] = i

                for side, idx in hand_idx.items():
                    if idx is not None:
                        for i in range(person.features.hand_landmarks_count):
                            coordinates = output.multi_hand_landmarks[idx].landmark[i]
                            coordinates = (coordinates.x, coordinates.y, coordinates.z)
                            if side == "Left":
                                subarray[i] = coordinates
                            elif side == "Right":
                                subarray[i+person.features.hand_landmarks_count] = coordinates
                            else:
                                assert False

                person.features.submit_hands_data(frame.capture_time, frame.id, subarray)
        except Exception as exception:
            self.__unpredicted_exception = exception

    def _extract_face_data(self, person: Person, frame: Frame):
        try:
            output = face_features_back_end.run(frame.data)
            if output.multi_face_landmarks:
                output = output.multi_face_landmarks[0]
                subarray = np.full((person.features.face_landmarks_count, person.features.dims), -1.0)
                for i in range(person.features.face_landmarks_count):
                    coordinates = output.landmark[i]
                    subarray[i] = coordinates.x, coordinates.y, coordinates.z
                person.features.submit_face_data(frame.capture_time, frame.id, subarray)
        except Exception as exception:
            self.__unpredicted_exception = exception

    def _process_frame(self, frame: Frame):
        threads = []
        for person in self.__people_tracker.get():
            cropped_frame = frame.crop(person.get_bbox())
            for func in [self._extract_hands_data, self._extract_face_data]:
                thread = Thread(
                        target=func,
                        args=(person, cropped_frame),
                        name=f"{func.__name__} - {uuid.uuid4()}",
                        daemon=True
                    )
                thread.start()
                threads.append(thread)

        for thread in threads:
            thread.join()

        if self.__unpredicted_exception is not None:
            raise UnpredictedException(self.__unpredicted_exception)

    def _run(self):
        try:
            self.__do_process = True
            timer = Timer(1 / FEATURES_EXTRACTION_FRAMES_PER_SEC)
            while self.__do_process:
                self._process_frame(self.__video_capture.get_frame())
                timer.wait()
        except (self.__video_capture.NotAvailable, self.__video_capture.EmptyFrame):
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
        self.__do_process = False
        self._thread.join()
        if self.__unpredicted_exception is not None:
            raise UnpredictedException(self.__unpredicted_exception)
