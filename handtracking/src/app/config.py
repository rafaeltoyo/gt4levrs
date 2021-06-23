
from mediapipe.python.solutions.hands import HandLandmark
from mediapipe.python.solutions.pose import PoseLandmark


class ServerConfig:
    protocol = "tcp"
    address = "*"
    port = 5555
    handshake = "handtracking"


class MediaPipePoseConfig:
    static_image_mode = False
    upper_body_only = False
    smooth_landmarks = True
    min_detection_confidence = 0.5
    min_tracking_confidence = 0.5


class MediaPipeHandConfig:
    static_image_mode = True
    max_num_hands = 2
    min_detection_confidence = 0.5
    min_tracking_confidence = 0.5


class HandPositionConfig:
    adjust_size = True
    adjust_z = True
    desired_scale_factor = 0.2
    field_of_view = 71
    min_xyz_value = 0
    max_xyz_value = 1
    id_first_joint = HandLandmark.MIDDLE_FINGER_MCP
    id_second_joint = HandLandmark.WRIST
    id_first_center_joint = PoseLandmark.LEFT_SHOULDER
    id_second_center_joint = PoseLandmark.RIGHT_SHOULDER
