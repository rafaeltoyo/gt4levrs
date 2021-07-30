import logging
import multiprocessing
import time
import cv2

from handtracking.src.app.config import DebugOption
from handtracking.src.app.threads import HandTrackingWorker, ServerWorker
from multiprocessing import Manager

from handtracking.src.app.utils.logging_manager import LoggingManager


class ThreadManager:
    def __init__(self):
        self.result_queue = Manager().Queue(maxsize=1)
        self.logger = LoggingManager.get_logger("ThreadManager", logging_level=logging.INFO)

        self.logger.info("Loaded camera")
        # Hand Tracking Thread
        mediapipe_process = HandTrackingWorker(
            self.result_queue,
            debug_console=DebugOption.debug_console,
            debug_video=DebugOption.debug_video,
            record_video=DebugOption.record_video
        )
        mediapipe_process.start()
        self.logger.info("Started handtracking process")

        # Server Thread
        server = ServerWorker(self.result_queue)
        server.start()
        self.logger.info("Started server worker")

        self.check_process_status()
        try:
            while True:
                time.sleep(10)
        finally:
            self.terminate_streams()

    def check_process_status(self):
        try:
            self.logger.info("Checking processes status . . .")

            retries = 5
            while True:
                process_list = multiprocessing.active_children()
                if len(process_list) >= 1:
                    for process in process_list:
                        self.check_if_process_is_alive(process)
                    retries = 5
                elif retries > 0:
                    self.logger.debug("There are no cameras in the camera list, retrying " + str(retries) + " times...")
                    retries -= 1
                else:
                    self.logger.info("There are no cameras in the camera list, terminating program!")
                    break
                time.sleep(5)
        finally:
            self.terminate_streams()

    def check_if_process_is_alive(self, process):
        status = False
        if not process.is_alive():
            for i in range(10):
                status = process.is_alive()
                if not status:
                    self.logger.warning("Process " + str(process) + " is not alive! Trying " + str(i) + " more times.")
                    time.sleep(5)
                if status:
                    break
            if not status:
                self.remove_streaming_process(process)

    def terminate_streams(self):
        self.logger.info("Terminating streams . . .")
        streams = multiprocessing.active_children()
        for stream_data in streams:
            streaming_id = stream_data
            self.remove_streaming_process(streaming_id)
        cv2.destroyAllWindows()
        self.logger.warning("Processes killed!")

    def remove_streaming_process(self, process):
        self.logger.info("Terminating stream process " + str(process))
        process.terminate()
