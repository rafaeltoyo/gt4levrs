from abc import ABC, abstractmethod
from typing import List, Optional

import cv2
import numpy as np

########################################################################################################################
from mediapipe.python.solutions.drawing_utils import draw_landmarks
from mediapipe.python.solutions.hands import HAND_CONNECTIONS, HandLandmark
from mediapipe.python.solutions.pose import POSE_CONNECTIONS

from handtracking.src.app.handler.hand_position_parser import HandPositionParser
from handtracking.src.app.handler.hand_selector_parser import HandSelectorParser
from handtracking.src.app.handler.wrapper import HandResultWrapper, BodyResultWrapper
from mediapipe.python.solutions.pose import Pose, PoseLandmark

from handtracking.src.app.mediapipeadapter.mp_utils import MediaPipePoseIndexMapper, MediaPipeHandIndexMapper
from mediapipe.python.solutions.holistic import Holistic


class HolisticHandler:

    def __init__(self):
        """

        Parameters
        ----------
        hand_handler
        body_handler
        debugging
        """
        self.frame_count = 0
        self.body_buffer_result = None
        self.holistic_handler = Holistic(static_image_mode=False,
                                         upper_body_only=False,
                                         smooth_landmarks=True,
                                         min_detection_confidence=0.5,
                                         min_tracking_confidence=0.5)
        self.hands_selector = HandSelectorParser()
        self.hands_adjustment = HandPositionParser()

    def get_parsed_result(self, image: np.ndarray, debugging: bool = False):
        unparsed_results, image = self.process(image, debugging=debugging)
        parsed_result = self.parse(unparsed_results)
        return parsed_result, image

    def process(self, image: np.ndarray, debugging: bool = False):
        # Flip the image horizontally for a later selfie-view display, and convert the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # To improve performance, optionally mark the image as not writeable to pass by reference.
        image.flags.writeable = False

        unparsed_holistic_results = self.holistic_handler.process(image)

        if debugging:
            image = self.debug(image, unparsed_holistic_results)

        return unparsed_holistic_results, image

    @staticmethod
    def debug(image, holistic_results):
        draw_landmarks(image, holistic_results.left_hand_landmarks, HAND_CONNECTIONS)
        draw_landmarks(image, holistic_results.right_hand_landmarks, HAND_CONNECTIONS)
        draw_landmarks(image, holistic_results.pose_landmarks, POSE_CONNECTIONS)
        return image

    def parse(self, unparsed_holistic_results):
        parsed_body = self.parse_body(unparsed_holistic_results)
        parsed_hands = self.parse_hands(unparsed_holistic_results)

        self.hands_selector.parse(parsed_hands, parsed_body)
        self.hands_adjustment.parse(parsed_body)

        return parsed_body

    @staticmethod
    def parse_body(holistic_results):
        """
        This method translate the result from MediaPipe Holistic to a body wrapper.
        Parameters
        ----------
        holistic_results Data from MediaPipe Holistic process.
        Returns
        -------
        Pose detected by MediaPipe.
        """

        if holistic_results is None or holistic_results.pose_landmarks is None:
            return BodyResultWrapper(size=0)

        wrapper = BodyResultWrapper(
            size=len(PoseLandmark),
            index_mapper=MediaPipePoseIndexMapper()
        )
        idx = 0
        for landmark in holistic_results.pose_landmarks.landmark:
            wrapper.add(PoseLandmark(idx).name,
                        idx,
                        landmark.x,
                        landmark.y,
                        landmark.z)
            idx += 1
        return wrapper

    def parse_hands(self, holistic_results: any) -> List[HandResultWrapper]:
        """
        This method translate the result from MediaPipe Holistic to a list of hands.
        Each hands is a wrapper of landmarks and handedness.

        Parameters
        ----------
        holistic_results Data from MediaPipe Holistic process.

        Returns
        -------
        List of hands detected by MediaPipe.
        """
        if holistic_results is None:
            return []

        parsed: List[HandResultWrapper] = []

        if holistic_results.left_hand_landmarks is not None:
            self.append_hand_to_result(holistic_results.left_hand_landmarks, "LEFT", parsed)

        if holistic_results.right_hand_landmarks is not None:
            self.append_hand_to_result(holistic_results.right_hand_landmarks, "RIGHT", parsed)

        return parsed

    def append_hand_to_result(self, hand_landmarks, handedness, parsed):
        handedness_dict = self.get_handedness_dict(handedness)

        wrapper = HandResultWrapper(
            handedness_dict["index"],
            handedness_dict["score"],
            handedness_dict["label"],
            index_mapper=MediaPipeHandIndexMapper()
        )
        idx = 0
        for landmark in hand_landmarks.landmark:
            wrapper.add(HandLandmark(idx).name,
                        idx,
                        landmark.x,
                        landmark.y,
                        landmark.z)
            idx += 1
        parsed.append(wrapper)

    @staticmethod
    def get_handedness_dict(handness_string):
        handedness_dict = {}
        if handness_string == "LEFT":
            handedness_dict["index"] = 0
        elif handness_string == "RIGHT":
            handedness_dict["index"] = 1
        handedness_dict["score"] = 0
        handedness_dict["label"] = handness_string
        return handedness_dict
