import math

import numpy as np

from ..config import HandPositionConfig
from .wrapper import BodyResultWrapper, HandResultWrapper


class HandPositionParser:
    """
    This class normalize the hands size using a desired scale factor.
    The difference between hand size and desired scale is going to adjust z coordinate.
    """
    ID_WRIST = 0
    ID_MIDDLE_MCP = 9

    def __init__(self,
                 adjust_size: bool = HandPositionConfig.adjust_size,
                 adjust_z: bool = HandPositionConfig.adjust_z,
                 desired_scale_factor: float = HandPositionConfig.desired_scale_factor,
                 ratio_between_palm_shoulder: float = HandPositionConfig.ratio_between_palm_shoulder,
                 field_of_view: float = HandPositionConfig.field_of_view,
                 palm_joint_ref1_id: int = HandPositionConfig.palm_joint_ref1,
                 palm_joint_ref2_id: int = HandPositionConfig.palm_joint_ref2,
                 left_shoulder_ref: int = HandPositionConfig.left_shoulder_ref,
                 right_shoulder_ref: int = HandPositionConfig.right_shoulder_ref,
                 min_xyz_value: float = HandPositionConfig.min_xyz_value,
                 max_xyz_value: float = HandPositionConfig.max_xyz_value):
        """

        :param adjust_size:
            Active size adjustment (normalization)
        :param adjust_z:
            Active z distance adjustment (estimate z based on size and field of view)
        :param desired_scale_factor:
            Expected distance between ref1 and ref2 joint.
            Pay attention on min and max values of coordinates.
        :param ratio_between_palm_shoulder:
            Ratio between palm size and shoulders distance
        :param field_of_view:
            Field of view of Video Capture.
            Value in degrees.
        :param palm_joint_ref1_id:
            First joint reference and normalize resizing pivot.
            This value is the joint position in hand data array.
        :param palm_joint_ref2_id:
            Second joint reference.
            This value is the joint position in hand data array.
        :param left_shoulder_ref:
            Left shoulder joint id
        :param right_shoulder_ref:
            Right shoulder joint id
        :param min_xyz_value:
            Min value for x, y and z.
        :param max_xyz_value:
            Max value for x, y and z.
        """
        self.adjust_size = adjust_size
        self.adjust_z = adjust_z
        self.desired_scale_factor = desired_scale_factor
        self.ratio_between_palm_shoulder = ratio_between_palm_shoulder
        self.field_of_view = field_of_view * math.pi / 180
        self.palm_joint_ref1_id = palm_joint_ref1_id
        self.palm_joint_ref2_id = palm_joint_ref2_id
        self.left_shoulder_ref = left_shoulder_ref
        self.right_shoulder_ref = right_shoulder_ref
        self.min_xyz_value = min_xyz_value
        self.max_xyz_value = max_xyz_value

    def parse(self, body: BodyResultWrapper) -> BodyResultWrapper:
        """
        :param body:
        :return:
        """

        shoulder_distance = 0
        if body.data is not None and body.data.shape[0] > 0:
            shoulder_distance = self.calculate_shoulder_distance(body.data)

        if body.left_hand:
            body.left_hand = self.parse_hand(body.left_hand, shoulder_distance)

        if body.right_hand:
            body.right_hand = self.parse_hand(body.right_hand, shoulder_distance)

        return body

    def parse_hand(self, hand: HandResultWrapper, shoulder_distance: float = 0) -> HandResultWrapper:
        """
        :param hand:
        :param shoulder_distance:
        :return:
        """
        if not hand or hand.data.shape[1] != 3:
            return hand
        if not self.adjust_size and not self.adjust_z:
            return hand

        # Calculate distance between ref1 and ref2
        actual_scale_factor = self.calculate_palm_size(hand.data)

        # Scale factor adjust (resizing)
        scale_factor_adjust = self.desired_scale_factor / actual_scale_factor

        # Normalization

        if self.adjust_size:
            # Hand reference for normalizing
            #pivot: np.ndarray = hand.data[self.palm_joint_ref1_id].copy()
            pivot = np.array([0.5, 0.5, 0.5], dtype="float")

            # Centralize joints at reference
            hand.data[:] -= pivot

            # Resize hand
            hand.data[:][:] *= scale_factor_adjust

            # Return the hand to original coordinate reference
            hand.data[:] += pivot

        # z adjustment
        if self.adjust_z:
            # Adjust the z coordinate
            # Bigger hands means more closer from webcam
            # Close means more further from you
            # Positive values of z means further from you
            if shoulder_distance > 0:
                real_palm_desired = shoulder_distance * self.ratio_between_palm_shoulder / actual_scale_factor
                hand.data[:] -= (0, 0, self._estimate_z(real_palm_desired))
            else:
                hand.data[:] -= (0, 0, self._estimate_z(scale_factor_adjust))

        return hand

    def _estimate_z(self, scale_factor: float):
        image_size = self.max_xyz_value - self.min_xyz_value
        return image_size * (1 - scale_factor) / (2 * math.tan(self.field_of_view / 2))

    def calculate_palm_size(self, hand_joints: np.ndarray):
        ref1: np.ndarray = hand_joints[self.palm_joint_ref1_id]
        ref2: np.ndarray = hand_joints[self.palm_joint_ref2_id]
        return np.sqrt(np.sum((ref1 - ref2) ** 2))

    def calculate_shoulder_distance(self, body_joints: np.ndarray):
        ref1: np.ndarray = body_joints[self.left_shoulder_ref]
        ref2: np.ndarray = body_joints[self.right_shoulder_ref]
        return np.sqrt(np.sum((ref1 - ref2) ** 2))
