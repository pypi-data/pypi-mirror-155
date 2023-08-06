import mediapipe as mp
import time
import cv2
from dermatillo.utils import BackEndDispatcher
from dermatillo.video_capture import VideoCapture
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh

a = BackEndDispatcher(
    mp.solutions.face_mesh.FaceMesh,
    {
        "refine_landmarks": True,
        "min_detection_confidence": 0.5,
        "min_tracking_confidence": 0.5,
        "max_num_faces": 1,
        "static_image_mode": True
    },
    back_ends_per_source=3,
    back_ends_per_source_max=10
)

b = BackEndDispatcher(
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

video_cap = VideoCapture(0)
video_cap.start()
start = time.time()
while time.time() - start < 30:
    frame = video_cap.get_frame().data
    x = time.time()
    output = a.run(frame)
    print(time.time() - x)
    image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    # if output.multi_hand_landmarks:
    #     for hand_landmarks in output.multi_hand_landmarks:
    #         mp_drawing.draw_landmarks(
    #             image,
    #             hand_landmarks,
    #             mp_hands.HAND_CONNECTIONS,
    #             mp_drawing_styles.get_default_hand_landmarks_style(),
    #             mp_drawing_styles.get_default_hand_connections_style())

    if output.multi_face_landmarks:
        for face_landmarks in output.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_tesselation_style())
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_contours_style())
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_IRISES,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_iris_connections_style())
    # Flip the image horizontally for a selfie-view display.
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
        break

video_cap.stop()