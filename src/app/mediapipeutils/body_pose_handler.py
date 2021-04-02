import mediapipe as mp
from mediapipe.python.solutions.pose import Pose
import mediapipe.python.solutions.drawing_utils as mp_drawing
import mediapipe.python.solutions.pose as mp_pose


class BodyPoseHandler:
    def __init__(self):
        self.body_pose_estimator = Pose(static_image_mode=False,
                                        upper_body_only=False,
                                        smooth_landmarks=True,
                                        min_detection_confidence=0.5,
                                        min_tracking_confidence=0.5)

    def process(self, input_frame) -> object:
        body_results = self.body_pose_estimator.process(input_frame)
        return body_results

    @staticmethod
    def print_result(image, results):
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
        return image

    def parse(self, body_results):
        if not body_results.pose_landmarks:
            return {}

        values = []

        # Add a dictionary with label and xyz coordinates for each joint in the pose
        for landmark in body_results.pose_landmarks.landmark:
            item = {
                "name": mp_pose.PoseLandmark(len(values)).name,
                "x": landmark.x,
                "y": landmark.y,
                "z": landmark.z
            }

            values.append(item)

        return values
