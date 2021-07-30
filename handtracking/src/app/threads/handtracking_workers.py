import logging
import multiprocessing
import os
import sys
import threading
import time
from queue import Queue, Empty

import cv2

from handtracking.src.app.handler import PoseHandler
from handtracking.src.app.mediapipeadapter import MediaPipeHandPoseHandler, MediaPipeBodyPoseHandler
from handtracking.src.app.utils.logging_manager import LoggingManager


class HandTrackingWorker(threading.Thread):
    """
    A class that represents a hand-tracking worker.
    This class receive a video capture and uses that for read frames.
    Each frame going to be process by Hand pose and Body pose estimator.
    """

    def __init__(self,
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
        threading.Thread.__init__(self)
        self.logger = LoggingManager.get_logger("HandtrackingWorkers", logging_level=logging.INFO)
        if record_video:
            self.load_video_writer()
        self.queue = queue

        self.debug_console = debug_console
        self.debug_video = debug_video
        self.record_video = record_video

        self.video_writer_in = None
        self.video_writer_out = None

    def load_video_writer(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_index = len(os.listdir("results")) // 2
        self.video_writer_in = cv2.VideoWriter("results/video_input" + str(video_index) + ".mp4",
                                               fourcc, 10, (640, 480), True)
        self.video_writer_out = cv2.VideoWriter("results/video_output" + str(video_index) + ".mp4",
                                                fourcc, 10, (640, 480), True)

    def run(self):
        if self.record_video:
            self.load_video_writer()
        self.handler = PoseHandler(MediaPipeHandPoseHandler(), MediaPipeBodyPoseHandler())
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        self.logger.info("Loaded videocapture")
        try:
            while self.cap.isOpened() and self.is_alive():
                start_time = time.time()
                # Get a new frame from webcam
                success, input_frame = self.cap.read()
                if not success:
                    continue

                self.logger.debug("Processing frame")
                # Process hand and body pose estimation
                parsed_result, debug_image = self.handler.get_parsed_result(input_frame, debugging=self.debug_video)

                # Flip and convert input frame colors
                debug_image = cv2.cvtColor(cv2.flip(debug_image, 1), cv2.COLOR_RGB2BGR)
                self.logger.debug("Converting debug image")

                key = cv2.waitKey(1)
                if self.debug_video:
                    cv2.imshow("Debugging results!", debug_image)
                if self.record_video:
                    self.video_writer_out.write(debug_image)
                    self.video_writer_in.write(input_frame)
                    if key == ord("q"):
                        sys.exit()

                self.logger.debug("Adding result to queue")
                try:
                    self.queue.get_nowait()
                except Empty:
                    pass
                finally:
                    payload = parsed_result.json()
                    self.queue.put_nowait(payload)
                    if self.debug_console:
                        fps_message = str(round(1 / (time.time() - start_time), 2)) + " fps"
                        self.logger.info(str(fps_message) + str(payload))
        finally:
            if self.cap is not None:
                self.cap.release()
            if self.video_writer_in is not None:
                self.video_writer_in.release()
            if self.video_writer_out is not None:
                self.video_writer_out.release()
            self.logger.info("Stopping HandTracking Worker!")
