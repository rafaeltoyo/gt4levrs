import os
import sys
import time
from queue import Queue, Empty
from threading import Thread

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
                 debug_console: bool = True,
                 debug_video: bool = False,
                 record_video: bool = False):
        """
        Create the Worker

        :param cap: Video Capture
        :param queue: Queue for parsed result
        :param debug_video: Active debugging mode. This worker going to show each frame read.
        :param record_video: Active recording mode. This worker going capture and save each frame. Only available when debug mode is on.
        """
        super().__init__(
            target=self._behaviour,
            args=[debug_console,
                  debug_video,
                  record_video],
            name="Server worker")
        self.cap = cap
        self.queue = queue
        self.handler = PoseHandler(MediaPipeHandPoseHandler(), MediaPipeBodyPoseHandler())
        self.video_writer_in = None
        self.video_writer_out = None
        if record_video:
            self.load_video_writer()

    def load_video_writer(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_index = len(os.listdir("results")) // 2
        self.video_writer_in = cv2.VideoWriter("results/video_input" + str(video_index) + ".mp4",
                                               fourcc, 10, (640, 480), True)
        self.video_writer_out = cv2.VideoWriter("results/video_output" + str(video_index) + ".mp4",
                                                fourcc, 10, (640, 480), True)

    def _behaviour(self, console: bool, debugging: bool, recording: bool):

        try:
            while self.cap.isOpened() and self.is_alive():
                start_time = time.time()

                # Get a new frame from webcam
                success, input_frame = self.cap.read()
                if not success:
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # Process hand and body pose estimation
                hands, body, debug_image = self.handler.process(input_frame, debugging=(debugging or recording))

                # Flip and convert input frame colors
                debug_image = cv2.cvtColor(cv2.flip(debug_image, 1), cv2.COLOR_RGB2BGR)

                if debugging or recording:
                    if debugging:
                        cv2.imshow("Debugging results!", debug_image)
                    if recording:
                        self.video_writer_out.write(debug_image)
                        self.video_writer_in.write(input_frame)
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
                    if console:
                        fps_message = str(round(1 / (time.time() - start_time), 2)) + " fps"
                        print(fps_message, payload)
        finally:
            if self.cap is not None:
                self.cap.release()
            if self.video_writer_in is not None:
                self.video_writer_in.release()
            if self.video_writer_out is not None:
                self.video_writer_out.release()
            print("Stopping HandTracking Worker!")
