
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
