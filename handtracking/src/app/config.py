
from mediapipe.python.solutions.hands import HandLandmark
from mediapipe.python.solutions.pose import PoseLandmark


class DebugOption:
    debug_video = False
    record_video = False
    debug_console = True


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
    desired_scale_factor = 0.1
    ratio_between_palm_shoulder = 0.3
    field_of_view = 71
    min_xyz_value = 0
    max_xyz_value = 1
    palm_joint_ref1 = HandLandmark.MIDDLE_FINGER_MCP
    palm_joint_ref2 = HandLandmark.WRIST
    left_shoulder_ref = PoseLandmark.LEFT_SHOULDER
    right_shoulder_ref = PoseLandmark.RIGHT_SHOULDER
