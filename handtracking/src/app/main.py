from queue import Queue

import cv2


from handtracking.src.app.ThreadManager import ThreadManager
from handtracking.src.app.config import DebugOption
from handtracking.src.app.threads import HandTrackingWorker, ServerWorker

process_manager = ThreadManager()


