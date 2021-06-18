from threading import Thread
from queue import Queue, Empty
import cv2

from app.handler import PoseHandler
from app.mediapipeadapter import MediaPipeHandPoseHandler, MediaPipeBodyPoseHandler


class HandTrackingWorker(Thread):
    """
    A class that represents a hand-tracking worker.
    This class receive a video capture and uses that for read frames.
    Each frame going to be process by Hand pose and Body pose estimator.
    """

    def __init__(self,
                 cap: cv2.VideoCapture,
                 queue: Queue,
                 show_image: bool = False):
        """
        Create the worker

        Parameters
        ----------
        cap
            Video Capture
        queue
            Queue for processed result
        show_image
            Active debug mode. This worker going to show each frame read.
        """
        self.cap = cap
        self.handler = PoseHandler(MediaPipeHandPoseHandler(),
                                   MediaPipeBodyPoseHandler())
        self.queue = queue
        super().__init__(
            target=self._behaviour,
            args=[show_image],
            name="Server worker")

    def _behaviour(self, debugging: bool):

        while self.cap.isOpened() and self.is_alive():

            # Get a new frame from webcam
            success, input_frame = self.cap.read()
            if not success:
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # Flip and convert input frame colors
            input_frame = cv2.cvtColor(cv2.flip(input_frame, 1), cv2.COLOR_RGB2BGR)

            # Process hand and body pose estimation
            hands, body, debug_image = self.handler.process(input_frame, debugging=debugging)

            if debugging:
                cv2.imshow("Debugging results!", debug_image)
                cv2.waitKey(1)

            # Parse results from MediaPipe
            parsed = self.handler.parse(hands, body)

            try:
                self.queue.get_nowait()
            except Empty:
                pass
            finally:
                payload = parsed.json()
                self.queue.put_nowait(payload)
                print(payload)

        self.cap.release()
        print("Stopping HandTracking Worker!")
