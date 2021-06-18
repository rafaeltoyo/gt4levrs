from queue import Queue

import cv2

from app.threads import ServerWorker, HandTrackingWorker

queue = Queue(maxsize=1)

# Hand Tracking Thread
process = HandTrackingWorker(cv2.VideoCapture(0), queue)
process.start()

# Server Thread
server = ServerWorker(queue)
server.start()
