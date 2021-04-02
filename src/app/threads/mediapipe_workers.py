from threading import Thread
from queue import Queue, Empty
import cv2
from src.app.mediapipeutils.body_pose_handler import BodyPoseHandler
from src.app.mediapipeutils.hand_pose_handler import HandPoseHandler


class MediapipeWorker(Thread):
    def __init__(self, cap: cv2.VideoCapture, queue: Queue, show_image: bool):
        self.cap = cap
        self.hand_pose_handler = HandPoseHandler(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.body_pose_handler = BodyPoseHandler()
        self.queue = queue
        super().__init__(
            target=self._behaviour,
            args=[show_image],
            name="Server worker")

    def _behaviour(self, print_results: bool):
        while self.cap.isOpened() and self.is_alive():
            # Get a new frame from webcam
            success, input_frame = self.cap.read()
            if not success:
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # Flip and convert input frame colors
            input_frame = self.preprocess(input_frame)

            # Process hand and body pose estimation
            body_results = self.body_pose_handler.process(input_frame=input_frame)
            hand_results = self.hand_pose_handler.process(input_frame=input_frame)

            # Parse mediapipe results into a format that unity will use
            mediapipe_results = self.parse_mediapipe_results(body_results, hand_results)

            if print_results:
                self.print_results(body_results, hand_results, input_frame)

            try:
                self.queue.get_nowait()
            except Empty:
                pass
            finally:
                self.queue.put_nowait(mediapipe_results)

        self.cap.release()
        print("Stopping HandTracking Worker!")

    def parse_mediapipe_results(self, body_results, hand_results):
        hand_results = self.hand_pose_handler.parse(hand_results)
        body_results = self.body_pose_handler.parse(body_results)
        mediapipe_results = {"hand_results": hand_results, "body_results": body_results}
        return mediapipe_results

    def preprocess(self, input_frame):
        input_frame = cv2.cvtColor(cv2.flip(input_frame, 1), cv2.COLOR_RGB2BGR)
        return input_frame

    def print_results(self, body_results, hand_results, input_frame):
        # Convert image to RGB format
        result_frame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2RGB)

        # Print and show hand and body poses results
        result_frame = self.body_pose_handler.print_result(result_frame, body_results)
        result_frame = self.hand_pose_handler.print_result(result_frame, hand_results)
        cv2.imshow("results", result_frame)
        cv2.waitKey(1)
