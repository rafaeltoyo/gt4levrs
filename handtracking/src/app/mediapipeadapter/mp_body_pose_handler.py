import numpy as np
import mediapipe as mp

from typing import Optional
from mediapipe.python.solutions.pose import Pose, PoseLandmark

from .mp_utils import MediaPipePoseIndexMapper
from ..handler.pose_handlers import BodyPoseHandler
from ..handler.wrapper import BodyResultWrapper


class MediaPipeBodyPoseHandler(BodyPoseHandler):
    """
    This class wrap the MediaPipe Pose solution and translate the result to recognized class of this project.
    """

    def __init__(self,
                 static_image_mode: bool = False,
                 upper_body_only: bool = False,
                 smooth_landmarks: bool = True,
                 min_detection_confidence: float = 0.5,
                 min_tracking_confidence: float = 0.5):
        super().__init__()

        self._solution = Pose(
            static_image_mode=static_image_mode,
            upper_body_only=upper_body_only,
            smooth_landmarks=smooth_landmarks,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence)

    def process(self, frame: np.ndarray):
        """
        Process a frame that contains a person and return the positions of his body joints

        Parameters
        ----------
        frame Frame from Video Capture

        Returns
        -------
        Protobuf from MediaPipe with body joints position
        """

        # To improve performance, optionally mark the image as not writeable to pass by reference.
        frame.flags.writeable = False

        return self._solution.process(frame)

    def parse(self, body) -> Optional[BodyResultWrapper]:
        """
        This method translate the result from MediaPipe to a body wrapper.

        Parameters
        ----------
        body Data from MediaPipe Pose process.

        Returns
        -------
        Pose detected by MediaPipe.
        """

        if body is None or body.pose_landmarks is None:
            return BodyResultWrapper(size=0)

        wrapper = BodyResultWrapper(
            size=len(PoseLandmark),
            index_mapper=MediaPipePoseIndexMapper()
        )
        idx = 0
        for landmark in body.pose_landmarks.landmark:
            wrapper.add(PoseLandmark(idx).name,
                        idx,
                        landmark.x,
                        landmark.y,
                        landmark.z)
            idx += 1
        return wrapper

    def close(self):
        """
        Close all resources
        """
        self._solution.close()

    def debug(self, image: np.ndarray, results: any):
        """
        Debug method
        """
        if results and results.pose_landmarks:
            mp_drawing = mp.solutions.drawing_utils
            mp_pose = mp.solutions.pose

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        return image
