import logging
from abc import ABC, abstractmethod

import numpy as np
import mediapipe as mp

from typing import Optional
from mediapipe.python.solutions.pose import Pose, PoseLandmark

from ..config import MediaPipePoseConfig
from .mp_utils import MediaPipePoseIndexMapper
from ..handler.wrapper import BodyResultWrapper
from ..utils.logging_manager import LoggingManager


class BodyPoseHandler(ABC):
    """
    This class must process a frame and parse the result into a body representation.
    """

    @abstractmethod
    def process(self, image: np.ndarray) -> any:
        pass

    @abstractmethod
    def parse(self, body: any) -> Optional[BodyResultWrapper]:
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def debug(self, image: np.ndarray, body: any):
        pass


class MediaPipeBodyPoseHandler(BodyPoseHandler):
    """
    This class wrap the MediaPipe Pose solution and translate the result to recognized class of this project.
    """

    def __init__(self,
                 static_image_mode: bool = MediaPipePoseConfig.static_image_mode,
                 upper_body_only: bool = MediaPipePoseConfig.upper_body_only,
                 smooth_landmarks: bool = MediaPipePoseConfig.smooth_landmarks,
                 min_detection_confidence: float = MediaPipePoseConfig.min_detection_confidence,
                 min_tracking_confidence: float = MediaPipePoseConfig.min_tracking_confidence):
        self.logger = LoggingManager.get_logger("HandtrackingWorkers", logging_level=logging.INFO)

        self._solution = Pose(
            static_image_mode=static_image_mode,
            upper_body_only=upper_body_only,
            smooth_landmarks=smooth_landmarks,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence)
        super().__init__()

    def process(self, frame: np.ndarray):
        frame.flags.writeable = False
        return self._solution.process(frame)

    def parse(self, body) -> Optional[BodyResultWrapper]:
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
        self._solution.close()

    def debug(self, image: np.ndarray, results: any):
        if results and results.pose_landmarks:
            mediapipe_drawing = mp.solutions.drawing_utils
            mediapipe_pose = mp.solutions.pose
            mediapipe_drawing.draw_landmarks(image, results.pose_landmarks, mediapipe_pose.POSE_CONNECTIONS)
        return image
