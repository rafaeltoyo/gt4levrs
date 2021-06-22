from abc import ABC, abstractmethod
from typing import List, Optional

import cv2
import numpy as np


########################################################################################################################
from app.handler.hand_position_parser import HandPositionParser
from app.handler.hand_selector_parser import HandSelectorParser
from app.handler.wrapper import HandResultWrapper, BodyResultWrapper


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
                 body_handler: BodyPoseHandler,
                 desired_scale_factor: float = HandPositionParser.DESIRED_SCALE_FACTOR,
                 field_of_view: float = HandPositionParser.FIELD_OF_VIEW,
                 joint_ref1_id: int = HandPositionParser.ID_MIDDLE_MCP,
                 joint_ref2_id: int = HandPositionParser.ID_WRIST,
                 min_xyz_value: float = HandPositionParser.MIN_XYZ_VALUE,
                 max_xyz_value: float = HandPositionParser.MAX_XYZ_VALUE):
        """

        Parameters
        ----------
        hand_handler
        body_handler
        debugging
        """
        self.hand_handler = hand_handler
        self.body_handler = body_handler
        self.hands_selector = HandSelectorParser()
        self.hands_adjustment = HandPositionParser(
            adjust_size=True,
            adjust_z=True,
            joint_ref1_id=joint_ref1_id,
            joint_ref2_id=joint_ref2_id,
            min_xyz_value=min_xyz_value,
            max_xyz_value=max_xyz_value,
            desired_scale_factor=desired_scale_factor,
            field_of_view=field_of_view)

    def process(self, image: np.ndarray, debugging: bool = False):
        # Flip the image horizontally for a later selfie-view display, and convert the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # To improve performance, optionally mark the image as not writeable to pass by reference.
        image.flags.writeable = False

        # Process
        hands = self.hand_handler.process(image)
        body = self.body_handler.process(image)

        if debugging:
            image.flags.writeable = True
            image = self.hand_handler.debug(image, hands)
            # image = self.body_handler.debug(image, body)

        return hands, body, image

    def parse(self, hands: any, body: any):
        parsed_hands = self.hand_handler.parse(hands)
        parsed_body = self.body_handler.parse(body)

        left_hand, right_hand = self.hands_selector.parse(parsed_hands)

        left_hand = self.hands_adjustment.parse(left_hand)
        right_hand = self.hands_adjustment.parse(right_hand)

        parsed_body.set_left_hand(left_hand)
        parsed_body.set_right_hand(right_hand)

        return parsed_body

########################################################################################################################
