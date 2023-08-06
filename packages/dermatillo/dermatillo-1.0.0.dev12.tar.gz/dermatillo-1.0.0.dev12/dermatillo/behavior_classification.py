import os
import numpy as np
import multiprocessing
from dermatillo.people_tracking import PeopleTracker
from dermatillo.utils import BackEndDispatcher
from dermatillo.config import *
from dermatillo.utils import get_platform, DERMATILLO_DIR

platform = get_platform()
if platform.name == "Linux":
    import tflite_runtime.interpreter as tflite
    Interpreter = tflite.Interpreter
elif platform.name == "macOS":
    import tensorflow as tf
    Interpreter = tf.lite.Interpreter

if os.environ.get("DERMATILLO_SETUP") != "1":
    from dermatillo.utils import alarm


class BehaviorClassifierBackEnd:
    def __init__(self) -> None:
        self._interpreter = Interpreter(
            model_path=os.path.join(DERMATILLO_DIR, "files/behavior_classifier.tflite"),
            num_threads=multiprocessing.cpu_count()
        )
        self._interpreter.allocate_tensors()
        self._input_index = self._interpreter.get_input_details()[0]["index"]
        self._output_index = self._interpreter.get_output_details()[0]["index"]

    def process(self, features: np.array) -> np.array:
        self._interpreter.set_tensor(self._input_index, features)
        self._interpreter.invoke()
        return self._interpreter.get_tensor(self._output_index)[0][1]


behavior_back_end = BackEndDispatcher(
    BehaviorClassifierBackEnd,
    {},
    back_ends_per_source=1,
    back_ends_per_source_max=1
)


class BehaviorClassifier:
    def __init__(self, people_tracker: PeopleTracker):
        self._people_tracker = people_tracker
        self._probabilities = []

    def _check_current_probability(self) -> None:
        probability = 0.
        for person in self._people_tracker.get():
            probability = max(probability, behavior_back_end.run(person.features.get_time_series()))
        self._probabilities.append(probability)

    def reset(self) -> None:
        self._probabilities = []

    def check(self) -> None:
        self._check_current_probability()
        if len(self._probabilities) >= int(TIME_SERIES_SECONDS / BEHAVIOR_CLASSIFICATION_PERIOD_SEC):
            assert len(self._probabilities) >= ALARM_ACTIVATION_STRIKE
            if all([prob > ALARM_ACTIVATION_THRESHOLD
                    for prob in self._probabilities[-ALARM_ACTIVATION_STRIKE:]]):
                alarm.trigger()
