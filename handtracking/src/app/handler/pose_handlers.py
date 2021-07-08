import logging
import cv2
import numpy as np

from .hand_position_parser import HandPositionParser
from .hand_selector_parser import HandSelectorParser
from .wrapper import BodyResultWrapper
from ..config import HandPositionConfig
from ..mediapipeadapter.mp_body_pose_handler import BodyPoseHandler
from ..mediapipeadapter.mp_hand_pose_handler import HandsPoseHandler
from ..utils.logging_manager import LoggingManager


class PoseHandler:

    def __init__(self,
                 hand_handler: HandsPoseHandler,
                 body_handler: BodyPoseHandler):
        self.frame_count = 0
        self.body_buffer_result = None
        self.logger = LoggingManager.get_logger("HandtrackingWorkers", logging_level=logging.INFO)

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
        hands = self.hand_handler.process(image)

        if self.frame_count % 5:
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
