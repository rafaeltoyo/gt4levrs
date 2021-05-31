import math

from google.protobuf.json_format import MessageToDict


class MediapipeResultNormalizer:
    DESIRED_SCALE_XY_FACTOR = 0.4

    @staticmethod
    def scale_xy_coordinate(hand_results):
        if hand_results is None or len(hand_results) == 0:
            return

        if "lhand" in hand_results:
            MediapipeResultNormalizer.scale_hand_joint_coordinate(hand_results, "lhand", "x")
            MediapipeResultNormalizer.scale_hand_joint_coordinate(hand_results, "lhand", "y")

        if "rhand" in hand_results:
            MediapipeResultNormalizer.scale_hand_joint_coordinate(hand_results, "rhand", "x")
            MediapipeResultNormalizer.scale_hand_joint_coordinate(hand_results, "rhand", "y")

    @staticmethod
    def scale_hand_joint_coordinate(hand_results, hand, coordinate):
        actual_scale_factor = MediapipeResultNormalizer.get_scale_factor(hand_results, hand, coordinate)
        if actual_scale_factor == 0:
            return

        scale_factor_adjust = MediapipeResultNormalizer.DESIRED_SCALE_XY_FACTOR / actual_scale_factor

        for joint_index in range(len(hand_results[hand]['joints'])):
            hand_results[hand]['joints'][joint_index][coordinate] *= scale_factor_adjust

        # Make sure it has the same scale factor
        # new_scale_factor = MediapipeResultNormalizer.get_scale_factor(hand_results, hand, coordinate)
        # print(actual_scale_factor, new_scale_factor)

    @staticmethod
    def scale_z_coordenate(hand_results):
        if len(hand_results) == 0:
            return

        if "lhand" in hand_results:
            MediapipeResultNormalizer.scale_hand_z_coordenate("lhand", hand_results)

        if "rhand" in hand_results:
            MediapipeResultNormalizer.scale_hand_z_coordenate("rhand", hand_results)

        return hand_results

    @staticmethod
    def scale_hand_z_coordenate(hand, results):
        x_scale_factor = MediapipeResultNormalizer.get_scale_factor(results, hand, "x")
        y_scale_factor = MediapipeResultNormalizer.get_scale_factor(results, hand, "y")
        if x_scale_factor == 0 or y_scale_factor == 0:
            return

        z_scale_factor = math.sqrt(x_scale_factor ** 2 + y_scale_factor ** 2)
        for joint_index in range(len(results[hand]['joints'])):
            results[hand]['joints'][joint_index]['z'] += z_scale_factor

        print(z_scale_factor)

    @staticmethod
    def get_scale_factor(results, hand, index):
        lhand_list_values = [joint[index] for joint in results[hand]['joints']]
        if len(lhand_list_values) <= 0:
            return 0

        max_joint_value = max(lhand_list_values)
        min_joint_value = min(lhand_list_values)
        scale_factor = abs(max_joint_value - min_joint_value)
        return scale_factor