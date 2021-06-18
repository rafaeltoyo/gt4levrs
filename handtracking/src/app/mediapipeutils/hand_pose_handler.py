import cv2
import mediapipe as mp
from mediapipe.python.solutions.hands import Hands

from . import HandPoseResultParser


class HandPoseHandler:

    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """ Hand tracking handler """
        self.hand_pose_estimator = Hands(
            max_num_hands=2,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.result_parser = HandPoseResultParser()

    def process(self, input_frame) -> object:
        """
        Process a frame that contains a person and return the positions of his hands

        Parameters
        ----------
        input_frame
            Frame from WebCam

        Returns
        -------
            Json with hands joints position
        """
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        input_frame.flags.writeable = False
        results = self.hand_pose_estimator.process(input_frame)
        return results

    def parse(self, hand_pose_results):
        return self.result_parser.parse_and_normalize(hand_pose_results)

    @staticmethod
    def print_result(image, results):
        if results == {}:
            return image

        mp_drawing = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        return image
