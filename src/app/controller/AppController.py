import cv2

import mediapipe as mp
import mediapipe.python.solutions.hands as mp_hands


class AppController:

    def __init__(self, cap: cv2.VideoCapture):
        self._cap = cap
        pass

    def run(self):
        pass

    def start_video(self):

        while self._cap.isOpened():

            success, image = self._cap.read()

            if not success:
                # Ignoring empty camera frame.
                continue

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = hands.process(image)

        self._cap.release()
