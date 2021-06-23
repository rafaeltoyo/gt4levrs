import math

import numpy as np

from ..config import HandPositionConfig
from app.handler.wrapper import HandResultWrapper


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
                 field_of_view: float = HandPositionConfig.field_of_view,
                 joint_ref1_id: int = HandPositionConfig.id_first_joint,
                 joint_ref2_id: int = HandPositionConfig.id_second_joint,
                 min_xyz_value: float = HandPositionConfig.min_xyz_value,
                 max_xyz_value: float = HandPositionConfig.max_xyz_value):
        """
        Parameters
        ----------
        adjust_size
            Active size adjustment (normalization)
        adjust_z
            Active z distance adjustment (estimate z based on size and field of view)
        desired_scale_factor
            Expected distance between ref1 and ref2 joint.
            Pay attention on min and max values of coordinates.
        field_of_view
            Field of view of Video Capture.
            Value in degrees.
        joint_ref1_id
            First joint reference and normalize resizing pivot.
            This value is the joint position in hand data array.
        joint_ref2_id
            Second joint reference.
            This value is the joint position in hand data array.
        min_xyz_value
            Min value for x, y and z.
        max_xyz_value
            Max value for x, y and z.
        """
        self.adjust_size = adjust_size
        self.adjust_z = adjust_z
        self.desired_scale_factor = desired_scale_factor
        self.field_of_view = field_of_view * math.pi / 180
        self.joint_ref1_id = joint_ref1_id
        self.joint_ref2_id = joint_ref2_id
        self.min_xyz_value = min_xyz_value
        self.max_xyz_value = max_xyz_value

    def parse(self, hand: HandResultWrapper) -> HandResultWrapper:
        """

        Parameters
        ----------
        hand

        Returns
        -------

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
            pivot: np.ndarray = hand.data[self.joint_ref1_id].copy()

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
            hand.data[:] -= (0, 0, self._estimate_z(scale_factor_adjust))

        return hand

    def _estimate_z(self, scale_factor: float):
        image_size = self.max_xyz_value - self.min_xyz_value
        return image_size * (1 - scale_factor) / (2 * math.tan(self.field_of_view / 2))

    def calculate_palm_size(self, hand_joints: np.ndarray):
        ref1: np.ndarray = hand_joints[self.joint_ref1_id]
        ref2: np.ndarray = hand_joints[self.joint_ref2_id]
        return np.sqrt(np.sum((ref1 - ref2) ** 2))
