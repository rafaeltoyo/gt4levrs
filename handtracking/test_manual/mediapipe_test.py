import cv2

from google.protobuf.json_format import MessageToDict

from mediapipe.python.solutions.drawing_utils import DrawingSpec, draw_landmarks
from mediapipe.python.solutions.hands import Hands, HAND_CONNECTIONS
from mediapipe.python.solutions.pose import Pose, POSE_CONNECTIONS

########################################################################################################################
# Test configuration

FLAG_SHOW_HANDS = True
FLAG_SHOW_BODY = True

LEFT_HAND_LANDMARK_COLOR = (0, 0, 255)
LEFT_HAND_CONNECTION_COLOR = (80, 80, 255)
RIGHT_HAND_LANDMARK_COLOR = (0, 255, 0)
RIGHT_HAND_CONNECTION_COLOR = (80, 255, 80)
BODY_LANDMARK_COLOR = (127, 155, 155)
BODY_CONNECTION_COLOR = (80, 127, 127)

########################################################################################################################
# MediaPipe models

hand_solution = Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

body_solution = Pose(
    static_image_mode=False,
    upper_body_only=False,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

########################################################################################################################
# Video Capture

cap = cv2.VideoCapture(0)

########################################################################################################################

while cap.isOpened():

    # Get a new frame
    success, image = cap.read()

    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

    # Flip the image horizontally for a later selfie-view display, and convert the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # To improve performance, optionally mark the image as not writeable to pass by reference.
    image.flags.writeable = False

    ####################################################################################################################
    # MediaPipe process

    hands_results = hand_solution.process(image) if FLAG_SHOW_HANDS else None
    body_results = body_solution.process(image) if FLAG_SHOW_BODY else None

    ####################################################################################################################
    # Draw the results

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if hands_results and hands_results.multi_hand_landmarks:
        for (hand_landmarks, handedness) in zip(hands_results.multi_hand_landmarks,
                                                hands_results.multi_handedness):
            handedness = MessageToDict(handedness)

            if handedness["classification"][0]["label"] == "Left":
                landmark_drawing_color = LEFT_HAND_LANDMARK_COLOR
                connection_drawing_color = LEFT_HAND_CONNECTION_COLOR
            elif handedness["classification"][0]["label"] == "Right":
                landmark_drawing_color = RIGHT_HAND_LANDMARK_COLOR
                connection_drawing_color = RIGHT_HAND_CONNECTION_COLOR
            else:
                landmark_drawing_color = (255, 255, 255)
                connection_drawing_color = (80, 80, 80)

            draw_landmarks(image,
                           hand_landmarks,
                           HAND_CONNECTIONS,
                           landmark_drawing_spec=DrawingSpec(color=landmark_drawing_color),
                           connection_drawing_spec=DrawingSpec(color=connection_drawing_color))

    if body_results and body_results.pose_landmarks:
        draw_landmarks(image,
                       body_results.pose_landmarks,
                       POSE_CONNECTIONS,
                       landmark_drawing_spec=DrawingSpec(color=BODY_LANDMARK_COLOR),
                       connection_drawing_spec=DrawingSpec(color=BODY_CONNECTION_COLOR))

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(1) & 0xFF == 27:
        break

hand_solution.close()
body_solution.close()
cap.release()
