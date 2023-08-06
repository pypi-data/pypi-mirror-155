import os
import sys
import time
from dermatillo.people_tracking import PeopleTracker
from dermatillo.utils import BackEndDispatcher
from dermatillo.utils import alarm
from dermatillo.config import *
from typing import Union

if sys.platform == "linux" and sys.version_info < (3, 10):
    import tflite_runtime.interpreter as tflite
    Interpreter = tflite.Interpreter
else:
    import tensorflow as tf
    Interpreter = tf.lite.Interpreter


class BehaviorClassifierBackEnd:
    def __init__(self):
        self._interpreter = Interpreter(
            model_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), "files/behavior_classifier.tflite"))
        self._interpreter.allocate_tensors()
        self._input_index = self._interpreter.get_input_details()[0]["index"]
        self._output_index = self._interpreter.get_output_details()[0]["index"]

    def process(self, features):
        self._interpreter.set_tensor(self._input_index, features)
        self._interpreter.invoke()
        return self._interpreter.get_tensor(self._output_index)[0][1]


face_features_back_end = BackEndDispatcher(
    BehaviorClassifierBackEnd,
    {},
    back_ends_per_source=1,
    back_ends_per_source_max=1
)


class BehaviorClassifier:
    def __init__(self, people_tracker: PeopleTracker):
        self._people_tracker = people_tracker
        self._triggered_at = 0.
        self._triggered = False
        self._probabilities = []

    def _check_current_probability(self):
        probability = 0.
        for person in self._people_tracker.get():
            probability = max(probability, face_features_back_end.run(person.features.get_time_series()))
        self._probabilities.append(probability)

    def reset(self):
        self._triggered = False
        self._probabilities = []

    def risk_increased(self) -> bool:
        if time.time() - self._triggered_at >= INCREASED_ALERT_TIME_OUT:
            return False
        else:
            return True

    def check(self):
        self._check_current_probability()
        if len(self._probabilities) >= int(TIME_SERIES_SECONDS / BEHAVIOR_CLASSIFICATION_PERIOD_SEC):
            assert len(self._probabilities) >= ALARM_ACTIVATION_STRIKE
            if all([prob > ALARM_ACTIVATION_THRESHOLD
                    for prob in self._probabilities[-ALARM_ACTIVATION_STRIKE:]]):
                alarm.trigger()
                self._triggered_at = time.time()
                self._triggered = True
                return self._triggered

    def is_unhealthy(self) -> Union[bool, None]:
        self._check_current_probability()

        if len(self._probabilities) >= int(TIME_SERIES_SECONDS / 2 / BEHAVIOR_CLASSIFICATION_PERIOD_SEC):
            assert len(self._probabilities) >= ALARM_ACTIVATION_STRIKE

            if all([prob > ALARM_ACTIVATION_THRESHOLD
                    for prob in self._probabilities[-ALARM_ACTIVATION_STRIKE:]]):
                alarm.trigger()
                self._triggered_at = time.time()
                self._triggered = True
                return self._triggered
            elif self._triggered:
                if len(self._probabilities) >= ALARM_DEACTIVATION_STRIKE:
                    if all([prob < ALARM_DEACTIVATION_THRESHOLD
                            for prob in self._probabilities[-ALARM_DEACTIVATION_STRIKE:]]):
                        return False
            else:
                return False

        return None
