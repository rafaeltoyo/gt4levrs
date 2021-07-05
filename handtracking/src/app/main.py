from queue import Queue

import cv2

from handtracking.src.app.config import DebugOption
from handtracking.src.app.threads import HandTrackingWorker, ServerWorker

queue = Queue(maxsize=1)

# Hand Tracking Thread
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

process = HandTrackingWorker(
    cap,
    queue,
    debug_console=DebugOption.debug_console,
    debug_video=DebugOption.debug_video,
    record_video=DebugOption.record_video
)
process.start()

# Server Thread
server = ServerWorker(queue)
server.start()

process.join(2)
server.join(2)
