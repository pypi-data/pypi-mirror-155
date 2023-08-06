import time
import numpy as np
import mediapipe as mp
from dermatillo.behavior_classification import BehaviorClassifierBackEnd
from dermatillo.utils import BackEndDispatcher


def benchmark_back_end(back_end: BackEndDispatcher, task: str, input_array: np.array, duration: int = 3) -> float:
    print(f"Benchmarking {task} back-end ...")

    # warm-up runs
    back_end.run(input_array)
    back_end.run(input_array)

    n = 0
    start = time.time()
    while time.time() - start < duration:
        back_end.run(input_array)
        n += 1
    finish = time.time()
    fps = n / (finish - start)
    print("  {:>10.2f} fps\n".format(fps))
    return fps


def run() -> None:
    back_end = BackEndDispatcher(
        mp.solutions.face_detection.FaceDetection,
        {"model_selection": 1, "min_detection_confidence": 0.5},
        back_ends_per_source=1,
        back_ends_per_source_max=1
    )
    benchmark_back_end(back_end, "face detection", np.random.randint(0, 256, (1080, 1920, 3)).astype(np.uint8))

    back_end = BackEndDispatcher(
        mp.solutions.face_mesh.FaceMesh,
        {
            "refine_landmarks": True,
            "min_detection_confidence": 0.5,
            "min_tracking_confidence": 0.5,
            "max_num_faces": 1,
            "static_image_mode": False
        },
        back_ends_per_source=1,
        back_ends_per_source_max=1
    )
    benchmark_back_end(back_end, "face features extraction", np.random.randint(0, 256, (1080, 1920, 3)).astype(np.uint8))

    back_end = BackEndDispatcher(
        mp.solutions.hands.Hands,
        {
            "model_complexity": 1,
            "min_detection_confidence": 0.5,
            "min_tracking_confidence": 0.5,
            "max_num_hands": 2,
            "static_image_mode": False
        },
        back_ends_per_source=1,
        back_ends_per_source_max=1
    )
    benchmark_back_end(back_end, "hand features extraction", np.random.randint(0, 256, (1080, 1920, 3)).astype(np.uint8))

    back_end = BackEndDispatcher(
        BehaviorClassifierBackEnd,
        {},
        back_ends_per_source=1,
        back_ends_per_source_max=1
    )
    benchmark_back_end(back_end, "behavior classification", np.random.rand(1, 128, 42, 4).astype(np.float32))
