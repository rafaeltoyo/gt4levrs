import os
import sys
import time
from queue import Queue, Empty
from threading import Thread

import cv2

from handtracking.src.app.handler import PoseHandler
from handtracking.src.app.mediapipeadapter import MediaPipeHandPoseHandler, MediaPipeBodyPoseHandler


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
        self.load_video_writer()
        self.cap = cap
        self.handler = PoseHandler(MediaPipeHandPoseHandler(), MediaPipeBodyPoseHandler())
        self.queue = queue
        super().__init__(
            target=self._behaviour,
            args=[show_image],
            name="Server worker")

    def load_video_writer(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_index = len(os.listdir("results")) // 2
        self.out = cv2.VideoWriter("results/video_output" + str(video_index) + ".mp4", fourcc, 10, (640, 480), True)
        self.input = cv2.VideoWriter("results/video_input" + str(video_index) + ".mp4", fourcc, 10, (640, 480), True)

    def _behaviour(self, debugging: bool):
        try:
            while self.cap.isOpened() and self.is_alive():
                start_time = time.time()

                # Get a new frame from webcam
                success, input_frame = self.cap.read()
                if not success:
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                start2_time = time.time()
                # Process hand and body pose estimation
                hands, body, debug_image = self.handler.process(input_frame, debugging=debugging)
                print(1 / (time.time() - start2_time))

                # Flip and convert input frame colors
                debug_image = cv2.cvtColor(cv2.flip(debug_image, 1), cv2.COLOR_RGB2BGR)

                if debugging:
                    cv2.imshow("Debugging results!", debug_image)
                    self.out.write(debug_image)
                    self.input.write(input_frame)
                    key = cv2.waitKey(1)
                    if key == ord("q"):
                        sys.exit()

                # Parse results from MediaPipe
                parsed = self.handler.parse(hands, body)

                try:
                    self.queue.get_nowait()
                except Empty:
                    pass
                finally:
                    payload = parsed.json()
                    self.queue.put_nowait(payload)
                    fps_message = str(round(1 / (time.time() - start_time), 2)) + " fps"
                    print(fps_message, payload)
        finally:
            self.cap.release()
            self.input.release()
            self.out.release()
            print("Stopping HandTracking Worker!")
