import logging
from abc import ABC, abstractmethod

import numpy as np
import mediapipe as mp

from typing import List
from mediapipe.python.solutions.hands import Hands, HandLandmark
from google.protobuf.json_format import MessageToDict


from ..config import MediaPipeHandConfig
from .mp_utils import MediaPipeHandIndexMapper
from ..handler.wrapper import HandResultWrapper
from ..utils.logging_manager import LoggingManager


class HandsPoseHandler(ABC):
    """
    This class must process a frame and parse the result into a list of hands.
    """

    @abstractmethod
    def process(self, image: np.ndarray) -> any:
        pass

    @abstractmethod
    def parse(self, hands: any) -> List[HandResultWrapper]:
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def debug(self, image: np.ndarray, hands: any):
        pass


class MediaPipeHandPoseHandler(HandsPoseHandler):
    """
    This class wrap the MediaPipe Hand solution and translate the result to recognized class of this project.
    """

    def __init__(self,
                 static_image_mode: bool = MediaPipeHandConfig.static_image_mode,
                 max_num_hands: int = MediaPipeHandConfig.max_num_hands,
                 min_detection_confidence: float = MediaPipeHandConfig.min_detection_confidence,
                 min_tracking_confidence: float = MediaPipeHandConfig.min_tracking_confidence):
        self.logger = LoggingManager.get_logger("HandtrackingWorkers", logging_level=logging.INFO)
        self.solution = Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence)

    def process(self, frame) -> any:
        """
        Process a frame that contains a person and return the positions of his hands

        Parameters
        ----------
        frame Frame from Video Capture

        Returns
        -------
        Protobuf from MediaPipe with hands joints position
        """

        # To improve performance, optionally mark the image as not writeable to pass by reference.
        frame.flags.writeable = False
        result = self.solution.process(frame)

        return result

    def parse(self, hands: any) -> List[HandResultWrapper]:
        """
        This method translate the result from MediaPipe to a list of hands.
        Each hands is a wrapper of landmarks and handedness.
        Parameters
        ----------
        hands Data from MediaPipe Hand process.
        Returns
        -------
        List of hands detected by MediaPipe.
        """
        if hands is None or hands.multi_hand_landmarks is None:
            return []

        parsed: List[HandResultWrapper] = []

        for (hand_landmarks, handedness) in zip(hands.multi_hand_landmarks, hands.multi_handedness):
            handedness = MessageToDict(handedness)
            wrapper = HandResultWrapper(
                handedness["classification"][0]["index"],
                handedness["classification"][0]["score"],
                handedness["classification"][0]["label"],
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
        return parsed

    def close(self):
        self.solution.close()

    def debug(self, image: np.ndarray, results: any):
        if results and results.multi_hand_landmarks:
            mp_drawing = mp.solutions.drawing_utils
            mp_hands = mp.solutions.hands
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        return image
