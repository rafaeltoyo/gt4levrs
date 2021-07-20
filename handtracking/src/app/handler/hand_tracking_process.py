import logging
import multiprocessing
import cv2
from mediapipe.python.solutions.hands import Hands
from handtracking.src.app.utils.logging_manager import LoggingManager


class HandTrackingProcess(multiprocessing.Process):
    def __init__(self):
        self.logger = LoggingManager.get_logger("handtracking process", logging_level=logging.INFO)
        multiprocessing.Process.__init__(self)

    def run(self):
        self.logger.info("processing")
        self._solution = Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5,
                               min_tracking_confidence=0.5)

        cap = cv2.VideoCapture(1)

        while True:
            status, frame = cap.read()

            if not status:
                break
            self.logger.info("processing")
            result = self._solution.process(frame)
            self.logger.info(str(result))


if __name__ == "__main__":
    handtrackingprocess = HandTrackingProcess()
    handtrackingprocess.start()
