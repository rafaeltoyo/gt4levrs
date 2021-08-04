import logging
from asyncio import Queue

from handtracking.src.app.config import DebugOption
from handtracking.src.app.threads import HandTrackingWorker, ServerWorker

from handtracking.src.app.utils.logging_manager import LoggingManager


class ThreadManager:
    def __init__(self):
        self.result_queue = Queue(maxsize=1)
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

    def remove_streaming_process(self, process):
        self.logger.info("Terminating stream process " + str(process))
        process.terminate()
