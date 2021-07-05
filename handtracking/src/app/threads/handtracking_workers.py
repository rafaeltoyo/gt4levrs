import os
import sys
import time
from queue import Queue, Empty
from threading import Thread

import cv2

from handtracking.src.app.handler import PoseHandler
from handtracking.src.app.handler.holistic_handler import HolisticHandler
from handtracking.src.app.mediapipeadapter import MediaPipeHandPoseHandler, MediaPipeBodyPoseHandler


class HandTrackingWorker(Thread):
    """
    A class that represents a hand-tracking worker.
    This class receive a video capture and uses that for read frames.
    Each frame going to be process by Hand pose and Body pose estimator.
    """

    def __init__(self, cap: cv2.VideoCapture, queue: Queue, show_image: bool = False, save_video: bool = False):
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
        if save_video:
            self.load_video_writer()
        self.cap = cap
        self.handler = PoseHandler(MediaPipeHandPoseHandler(), MediaPipeBodyPoseHandler())
        # self.handler = HolisticHandler()

        self.queue = queue
        super().__init__(
            target=self._behaviour,
            args=[show_image, save_video],
            name="Server worker")

    def load_video_writer(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_index = len(os.listdir("results")) // 2
        self.out = cv2.VideoWriter("results/video_output" + str(video_index) + ".mp4", fourcc, 10, (640, 480), True)
        self.input = cv2.VideoWriter("results/video_input" + str(video_index) + ".mp4", fourcc, 10, (640, 480), True)

    def _behaviour(self, debugging: bool, save_video: bool):
        try:
            while self.cap.isOpened() and self.is_alive():
                start_time = time.time()

                # Get a new frame from webcam
                success, input_frame = self.cap.read()
                if not success:
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # Process hand and body pose estimation
                parsed_result, debug_image = self.handler.get_parsed_result(input_frame, debugging=debugging)

                # Flip and convert input frame colors
                debug_image = cv2.cvtColor(cv2.flip(debug_image, 1), cv2.COLOR_RGB2BGR)

                if debugging:
                    cv2.imshow("Debugging results!", debug_image)
                    key = cv2.waitKey(1)
                    if key == ord("q"):
                        sys.exit()
                if save_video:
                    self.out.write(debug_image)
                    self.input.write(input_frame)

                try:
                    self.queue.get_nowait()
                except Empty:
                    pass
                finally:
                    payload = parsed_result.json()
                    self.queue.put_nowait(payload)
                    fps_message = str(round(1 / (time.time() - start_time), 2)) + " fps"
                    print(fps_message, payload)
        finally:
            self.cap.release()
            self.input.release()
            self.out.release()
            print("Stopping HandTracking Worker!")
