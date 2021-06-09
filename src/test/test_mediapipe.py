# Imports
import cv2
import mediapipe as mp
from app.mediapipeutils import HandPoseResultParser
from mediapipe.python.solutions.pose import Pose

from app.mediapipeutils.mediapipe_result_normalizer import MediapipeResultNormalizer

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

########################################################################################################################
# For webcam input:
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

bodyy = Pose(
    static_image_mode=False,
    upper_body_only=False,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

########################################################################################################################
# Webcam
cap = cv2.VideoCapture(0)

########################################################################################################################

while cap.isOpened():

    # get a new frame from webcam
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)
    body_results = bodyy.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    hand_index = 0
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            print(hand_landmarks)
            if hand_index == 0:
                mp_drawing.draw_landmarks(image,
                                          hand_landmarks,
                                          mp_hands.HAND_CONNECTIONS,
                                          landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255)),
                                          connection_drawing_spec=mp_drawing.DrawingSpec(color=(80, 80, 255)))
            else:
                mp_drawing.draw_landmarks(image,
                                          hand_landmarks,
                                          mp_hands.HAND_CONNECTIONS,
                                          landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0)),
                                          connection_drawing_spec=mp_drawing.DrawingSpec(color=(80, 255, 80)))
            hand_index += 1

    parser = HandPoseResultParser()

    if body_results.pose_landmarks:
        for landmark in body_results.pose_landmarks.landmark:
            hand_parsed_result = parser.parse_and_normalize(results)

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(1) & 0xFF == 27:
        break

hands.close()
cap.release()
