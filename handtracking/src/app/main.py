from queue import Queue

import cv2

from app.threads import HandTrackingWorker, ServerWorker
from app.config import DebugOption

queue = Queue(maxsize=1)

# Hand Tracking Thread
process = HandTrackingWorker(
    cv2.VideoCapture(0),
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
