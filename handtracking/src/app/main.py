from queue import Queue

import cv2

from handtracking.src.app.threads import HandTrackingWorker, ServerWorker

queue = Queue(maxsize=1)

process = HandTrackingWorker(cap=cv2.VideoCapture(0), queue=queue, show_image=True, save_video=False)
server = ServerWorker(queue)

try:
    # Hand Tracking Thread
    process.start()

    # Server Thread
    server.start()

finally:
    server.join(2)
    process.join(2)
