import logging
import os
import sys
import threading
import time
import numpy as np
from asyncio import QueueEmpty
from queue import Queue, Empty

import cv2

from ..handler import PoseHandler
from ..mediapipeadapter import MediaPipeHandPoseHandler, MediaPipeBodyPoseHandler
from ..utils.logging_manager import LoggingManager


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

        # My Webcam
        #video_size = (640, 480)
        video_size = (1920, 1080)

        video_input_name = "results/video_input_{}.mp4".format(video_index)
        self.video_writer_in = cv2.VideoWriter(video_input_name, fourcc, 10, video_size, True)

        video_output_name = "results/video_output_{}.mp4".format(video_index)
        self.video_writer_out = cv2.VideoWriter(video_output_name, fourcc, 10, video_size, True)

    def run(self):
        if self.record_video:
            self.load_video_writer()

        self.handler = PoseHandler(MediaPipeHandPoseHandler(), MediaPipeBodyPoseHandler())

        self.cap = cv2.VideoCapture("D:\\Workspace\\tcc\\Recording\\tests\\medium\\pray\\original.mp4")
        #self.cap = cv2.VideoCapture(0)

        cv2.imshow("Debugging results!", np.ndarray([]))

        while True:
            key = cv2.waitKey(100)
            if key == ord("q"):
                break

        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        self.logger.info("Loaded videocapture")
        try:
            while self.cap.isOpened() and self.is_alive():
                start_time = time.time()
                # Get a new frame from webcam
                success, input_frame = self.cap.read()

                if not success:
                    key = cv2.waitKey(100)
                    if key == ord("q"):
                        break
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
                        break

                self.logger.debug("Adding result to queue")
                try:
                    self.queue.get_nowait()
                except QueueEmpty:
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

        sys.exit(0)
