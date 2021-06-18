import cv2

from app.mediapipe import MediaPipeHandPoseHandler, MediaPipeBodyPoseHandler

########################################################################################################################
# MediaPipe models

hand_solution = MediaPipeHandPoseHandler(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

pose_solution = MediaPipeBodyPoseHandler(
    static_image_mode=False,
    upper_body_only=False,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

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

    hands = hand_solution.process(image)
    pose = pose_solution.process(image)

    hands_parsed = hand_solution.parse(hands)
    pose_parsed = pose_solution.parse(pose)

    if hands_parsed:
        for item in hands_parsed:
            print(item.json())
    if pose_parsed:
        print(pose_parsed.json())

    ####################################################################################################################
    # Draw the results

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    image = MediaPipeHandPoseHandler.print_result(image, hands)
    image = MediaPipeBodyPoseHandler.print_result(image, pose)

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(1) & 0xFF == 27:
        break

hand_solution.close()
cap.release()
