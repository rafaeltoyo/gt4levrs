from abc import ABC, abstractmethod
from typing import List, Optional

import cv2
import numpy as np

from .hand_position_parser import HandPositionParser
from .hand_selector_parser import HandSelectorParser
from .wrapper import BodyResultWrapper, HandResultWrapper
from ..config import HandPositionConfig

########################################################################################################################


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


########################################################################################################################

class BodyPoseHandler(ABC):
    """
    This class must process a frame and parse the result into a body representation.
    """

    @abstractmethod
    def process(self, image: np.ndarray) -> any:
        pass

    @abstractmethod
    def parse(self, body: any) -> Optional[BodyResultWrapper]:
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def debug(self, image: np.ndarray, body: any):
        pass


########################################################################################################################

class PoseHandler:

    def __init__(self,
                 hand_handler: HandsPoseHandler,
                 body_handler: BodyPoseHandler):
        """

        Parameters
        ----------
        hand_handler
        body_handler
        debugging
        """
        self.frame_count = 0
        self.body_buffer_result = None

        self.hand_handler = hand_handler
        self.body_handler = body_handler
        self.hands_selector = HandSelectorParser()
        self.hands_adjustment = HandPositionParser()

    def get_parsed_result(self, image: np.ndarray, debugging: bool = False):
        hands_result, body_result, image = self.process(image, debugging=debugging)
        parsed_result = self.parse(hands_result, body_result)
        return parsed_result, image

    def process(self, image: np.ndarray, debugging: bool = False):
        # Flip the image horizontally for a later selfie-view display, and convert the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # To improve performance, optionally mark the image as not writeable to pass by reference.
        image.flags.writeable = False

        # Process
        hands = self.hand_handler.process(image)

        if self.frame_count % 5 == 0:
            self.body_buffer_result = self.body_handler.process(image)

        if debugging:
            image.flags.writeable = True
            image = self.hand_handler.debug(image, hands)
            image = self.body_handler.debug(image, self.body_buffer_result)

        self.frame_count += 1

        return hands, self.body_buffer_result, image

    def parse(self, hands: any, body: any):
        parsed_hands = self.hand_handler.parse(hands)
        parsed_body = self.body_handler.parse(body)

        self.hands_selector.parse(parsed_hands, parsed_body)
        self.hands_adjustment.parse(parsed_body)

        return parsed_body

    @staticmethod
    def _calculate_desired_adjustment_factor(parsed_body: BodyResultWrapper):
        ref1 = parsed_body.data[HandPositionConfig.left_shoulder_ref]
        ref2 = parsed_body.data[HandPositionConfig.right_shoulder_ref]

        distance = np.sqrt(np.sum((ref1 - ref2) ** 2))
        return distance * HandPositionConfig.desired_scale_factor


########################################################################################################################
