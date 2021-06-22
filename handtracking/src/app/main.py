from queue import Queue

import cv2

from app.threads import HandTrackingWorker, ServerWorker

queue = Queue(maxsize=1)

# Hand Tracking Thread
process = HandTrackingWorker(cv2.VideoCapture(0), queue, show_image=True)
process.start()

# Server Thread
server = ServerWorker(queue)
server.start()

process.join(2)
server.join(2)
