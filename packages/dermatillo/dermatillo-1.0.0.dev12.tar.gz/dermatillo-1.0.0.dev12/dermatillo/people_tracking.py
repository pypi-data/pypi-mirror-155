import threading
import time
import numpy as np
from dermatillo.objects import BBox, Person
from dermatillo.config import *


class PeopleTracker:
    def __init__(self):
        self.__tracked_people = []
        self.__lock = threading.Lock()

    def __remove_expired(self, reference_time: float, ignore_lock: bool = False):
        if not ignore_lock:
            self.__lock.acquire()
        self.__tracked_people = [
            person for person in self.__tracked_people
            if reference_time - person.time_last_seen < PERSON_TRACKING_TIME_OUT_SEC
        ]
        if not ignore_lock:
            self.__lock.release()

    def process_bboxes(self, capture_time: float, bboxes: list[BBox]):
        self.__lock.acquire()
        self.__remove_expired(capture_time, ignore_lock=True)

        assert len(bboxes) > 0
        if len(self.__tracked_people) > 0:
            iou_matrix = np.zeros((len(self.__tracked_people), len(bboxes)))
            mask = np.full(iou_matrix.shape, False)
            for i, person in enumerate(self.__tracked_people):
                for j, new_bbox in enumerate(bboxes):
                    iou_matrix[i][j] = person.get_bbox().calc_iou(new_bbox)
            unmatched_bbox_ids = [i for i in range(len(bboxes))]

            while np.max(iou_matrix) > 0. and not mask.all():
                person_idx, new_bbox_idx = np.unravel_index(iou_matrix.argmax(), iou_matrix.shape)
                self.__tracked_people[person_idx].update_position(capture_time, bboxes[new_bbox_idx])
                unmatched_bbox_ids.remove(new_bbox_idx)
                mask[person_idx, :] = True
                mask[:, new_bbox_idx] = True
                iou_matrix = np.ma.masked_array(iou_matrix, mask)

            for bbox_idx in unmatched_bbox_ids:
                self.__tracked_people.append(Person(capture_time, bboxes[bbox_idx]))
        else:
            for bbox in bboxes:
                self.__tracked_people.append(Person(capture_time, bbox))

        self.__lock.release()

    def get(self) -> list[Person]:
        self.__remove_expired(time.time())
        return self.__tracked_people
