from __future__ import annotations
import uuid
import time
import numpy as np
import threading
from dermatillo_pp import pre_process
from dermatillo.config import *


class BBox:
    def __init__(self, x_min: float, x_max: float, y_min: float, y_max: float):
        for args, vals in {("x_min", "x_max"): (x_min, x_max), ("y_min", "y_max"): (y_min, y_max)}.items():
            if vals[0] >= vals[1]:
                raise self.ImpossibleShape(args, vals)
        for arg, val in {"x_min": x_min, "x_max": x_max, "y_min": y_min, "y_max": y_max}.items():
            if not 0. <= val <= 1.0:
                raise self.OutOfRange(arg, val)

        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

        self.width = x_max - x_min
        self.height = y_max - y_min
        self.area = self.width * self.height

    class ImpossibleShape(Exception):
        def __init__(self, args: tuple[str, str], vals: tuple[float, float]):
            super().__init__(f"{args[0]} >= {args[1]} ({vals[0]} >= {vals[1]})")

    class OutOfRange(Exception):
        def __init__(self, arg: str, val: float):
            super().__init__(f"{arg} value ({val}) not in range of 0.0 <> 1.0")

    def calc_iou(self, other_bbox: BBox) -> float:
        intersection_width = max(0., min(self.x_max, other_bbox.x_max) - max(self.x_min, other_bbox.x_min))
        intersection_height = max(0., min(self.y_max, other_bbox.y_max) - max(self.y_min, other_bbox.y_min))
        intersection_area = intersection_height * intersection_width
        iou = intersection_area / (self.area + other_bbox.area - intersection_area)
        assert 0. <= iou <= 1.0
        return iou


class Features:
    def __init__(self):
        self.time_window = 1. / TIME_SERIES_POINTS_PER_SEC
        self.max_position = TIME_SERIES_POINTS_COUNT - 1
        self.hand_landmarks_count = 21
        self.face_landmarks_count = 468
        self.dims = 3

        self._lock = threading.Lock()

        self._feature_arrays = []
        self._time_series_positions = []
        self._latest_capture_time = None
        self._latest_frame_id = None

    class OverdueSubmission(Exception):
        pass

    class PositionOccupied(Exception):
        pass

    def _calc_shift(self, previous_capture_time: float, capture_time: float) -> int:
        """
        Calculate position shift in time series array relative to previous data point.

        Examples (assuming time window of 0.1 second)
        --------
        4.83 -> 5.0 lower tail = 2, 5.0 -> 6.0 full_seconds = 1, 6.0 -> 6.71 upper_tail = 7
        lower_tail (2) + full_seconds (1) * points_per_second (10) + upper_tail (7) = 19
        >>> self._calc_shift(4.83, 6.71)
        19
        >>> self._calc_shift(4.0, 7.0)
        30
        >>> self._calc_shift(4.0, 5.0)
        10
        >>> self._calc_shift(4.21, 4.25)
        0
        >>> self._calc_shift(4.37, 4.99)
        6
        >>> self._calc_shift(4.37, 5.0)
        7
        """
        def extract_decimal(value: float) -> float:
            return value - int(value)

        def calc_lower_tail() -> int:
            if capture_time < int(previous_capture_time + 1):
                upper_value_lower_tail = extract_decimal(capture_time)
            else:
                upper_value_lower_tail = 1.0
            lower_value_lower_tail = extract_decimal(previous_capture_time)
            return int(upper_value_lower_tail / self.time_window) - int(lower_value_lower_tail / self.time_window)

        def calc_upper_tail() -> int:
            if int(capture_time) > int(previous_capture_time):  # determine if upper tail present
                return int(extract_decimal(capture_time) / self.time_window)
            else:
                return 0

        assert capture_time >= 0 and previous_capture_time >= 0
        assert capture_time >= previous_capture_time
        full_seconds = max(0, int(capture_time) - int(previous_capture_time + 1))
        tail = calc_lower_tail() + calc_upper_tail()
        return full_seconds * TIME_SERIES_POINTS_PER_SEC + tail

    def _prepare_position(self, capture_time: float, frame_id: uuid.uuid4):
        input_subarray = np.full(
            (2 * self.hand_landmarks_count + self.face_landmarks_count, self.dims), -1.0)

        if len(self._feature_arrays) == 0:
            position = 0
        else:
            if capture_time < self._latest_capture_time:
                raise self.OverdueSubmission(self._latest_capture_time, capture_time)

            shift = self._calc_shift(self._latest_capture_time, capture_time)
            assert shift >= 0
            if shift == 0:
                raise self.PositionOccupied
            else:
                position = self._time_series_positions[-1] + shift

        self._feature_arrays.append(input_subarray)
        self._time_series_positions.append(position)
        self._latest_capture_time = capture_time
        self._latest_frame_id = frame_id

    def _get_index(self, capture_time: float, frame_id: uuid.uuid4) -> int:
        assert len(self._feature_arrays) == len(self._time_series_positions)
        if frame_id == self._latest_frame_id:
            if len(self._feature_arrays) == 0:
                raise self.OverdueSubmission
        else:
            self._prepare_position(capture_time, frame_id)
        return len(self._feature_arrays) - 1

    def get_time_series(self) -> np.array:
        time_series_array = np.zeros(
            (1, TIME_SERIES_POINTS_COUNT, 2*self.hand_landmarks_count, self.dims+1), dtype=np.float32)
        self._lock.acquire()
        if len(self._time_series_positions) > 0:
            shift_range = max(0, self._time_series_positions[-1] - self.max_position)
            shift_time = self._calc_shift(self._latest_capture_time, time.time())
            shift = shift_range + shift_time
            idx_to_crop_at = 0

            for i in reversed(range(len(self._feature_arrays))):
                if self._time_series_positions[i] - shift >= 0:
                    self._time_series_positions[i] -= shift
                    time_series_array[0][self._time_series_positions[i]] = pre_process(self._feature_arrays[i])
                else:
                    idx_to_crop_at = i
                    break

            del self._feature_arrays[:idx_to_crop_at+1]
            del self._time_series_positions[:idx_to_crop_at+1]
        self._lock.release()
        return time_series_array

    def submit_hands_data(self, capture_time: float, frame_id: uuid.uuid4, features_array: np.array):
        assert features_array.shape[0] == 2 * self.hand_landmarks_count
        assert features_array.shape[1] == self.dims

        self._lock.acquire()
        try:
            index = self._get_index(capture_time, frame_id)
            self._feature_arrays[index][:2 * self.hand_landmarks_count] = features_array
        except (self.PositionOccupied, self.OverdueSubmission):
            pass
        self._lock.release()

    def submit_face_data(self, capture_time: float, frame_id: uuid.uuid4, features_array: np.array):
        assert features_array.shape[0] == self.face_landmarks_count
        assert features_array.shape[1] == self.dims
        self._lock.acquire()
        try:
            index = self._get_index(capture_time, frame_id)
            self._feature_arrays[index][2 * self.hand_landmarks_count:] = features_array
        except (self.PositionOccupied, self.OverdueSubmission):
            pass
        self._lock.release()


class Person:
    """
    Kinda sad that this class landed in objects.py file. Such are the times...


    """
    def __init__(self, capture_time: float, bbox: BBox):
        self.features = Features()
        self.id = uuid.uuid4()
        self.time_last_seen = capture_time
        self.__bbox = bbox

    def get_bbox(self) -> BBox:
        return self.__bbox

    def update_position(self, capture_time: float, bbox: BBox):
        self.time_last_seen = capture_time
        self.__bbox = bbox


class Frame:
    def __init__(self, capture_time: time.time, data: np.array, identifier: uuid.uuid4 = None):
        self.capture_time = capture_time
        self.data = data
        self.id = uuid.uuid4() if identifier is None else identifier

    def crop(self, bbox: BBox) -> Frame:
        def convert_to_absolute(origin_size, relative_value):
            origin_size -= 1  # due to 0-based indexing of np arrays
            return int(origin_size * relative_value)

        assert self.data.ndim == 3
        frame_height = self.data.shape[0]
        frame_width = self.data.shape[1]
        y_min = convert_to_absolute(frame_height, bbox.y_min)
        y_max = convert_to_absolute(frame_height, bbox.y_max)
        x_min = convert_to_absolute(frame_width, bbox.x_min)
        x_max = convert_to_absolute(frame_width, bbox.x_max)
        new_data = self.data[y_min:y_max, x_min:x_max, :]

        return Frame(self.capture_time, new_data, self.id)
