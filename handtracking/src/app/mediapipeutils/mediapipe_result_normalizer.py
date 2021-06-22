import math


class MediapipeResultNormalizer:

    DESIRED_SCALE_XY_FACTOR = 0.2
    MAX_XYZ_VALUE = 1
    ID_WRIST = 0
    ID_MIDDLE_MCP = 9

    def __init__(self,
                 desired_scale_factor=DESIRED_SCALE_XY_FACTOR,
                 max_xyz_value=MAX_XYZ_VALUE,
                 joint_ref1_id=ID_MIDDLE_MCP,
                 joint_ref2_id=ID_WRIST):
        """
        Parameters
        ----------
        desired_scale_factor
            Expected distance between ref1 and ref2 joint
        max_xyz_value
            Max value for x, y and z
        joint_ref1_id
            First joint reference and normalize resizing pivot
        joint_ref2_id
            Second joint reference
        """
        self.desired_scale_factor = desired_scale_factor
        self.average_xyz_value = max_xyz_value / 2
        self.joint_ref1_id = joint_ref1_id
        self.joint_ref2_id = joint_ref2_id

    def normalize(self, hands):
        """

        Parameters
        ----------
        hands:
            Hands result from Mediapipe result parser

        Returns
        -------

        """
        if hands is None or len(hands) == 0:
            return hands
        if 'lhand' in hands:
            self.normalize_hand(hands['lhand'])
        if 'rhand' in hands:
            self.normalize_hand(hands['rhand'])
        return hands

    def normalize_hand(self, hand) -> None:
        """

        Parameters
        ----------
        hand

        Returns
        -------

        """
        if (hand is None) or ('joints' not in hand) or (len(hand['joints']) == 0):
            return

        # Calculate distance between ref1 and ref2
        actual_scale_factor = self.calculate_palm_size(hand['joints'])
        # Scale factor adjust (resizing)
        scale_factor_adjust = self.desired_scale_factor / actual_scale_factor
        # Delta factor adjust (z distance)
        delta_factor_adjust = actual_scale_factor

        # Hand reference for normalizing
        pivot_ref = hand['joints'][self.joint_ref1_id]
        pivot = {
            'x': pivot_ref['x'],
            'y': pivot_ref['y'],
            'z': pivot_ref['z']
        }

        # Centralize joints at ref1
        self.sum_xyz_values(hand['joints'],
                            {
                                'x': pivot['x'] * -1,
                                'y': pivot['y'] * -1,
                                'z': pivot['z'] * -1
                            })

        # Resize hand
        self.multiply_xyz_values(hand['joints'], scale_factor_adjust)

        # Return the hand to original coordinate reference
        self.sum_xyz_values(hand['joints'],
                            {
                                'x': pivot['x'],
                                'y': pivot['y'],
                                'z': pivot['z']
                            })

        # Adjust the z coordinate
        self.sum_xyz_values(hand['joints'], {
            'x': 0,
            'y': 0,
            'z': - delta_factor_adjust
        })

    def calculate_palm_size(self, hand_joints):
        ref1 = hand_joints[self.joint_ref1_id]
        ref2 = hand_joints[self.joint_ref2_id]
        return math.sqrt(
            math.pow(ref1['x'] - ref2['x'], 2)
            +
            math.pow(ref1['y'] - ref2['y'], 2)
            +
            math.pow(ref1['z'] - ref2['z'], 2)
        )

    @staticmethod
    def sum_xyz_values(hand_joints: list, value: dict) -> None:
        for joint in hand_joints:
            joint['x'] += value['x']
            joint['y'] += value['y']
            joint['z'] += value['z']

    @staticmethod
    def multiply_xyz_values(hand_joints: list, value: float) -> None:
        for joint in hand_joints:
            joint['x'] *= value
            joint['y'] *= value
            joint['z'] *= value
