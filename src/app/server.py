from queue import Queue

import cv2

from app.threads import ServerWorker, HandTrackingWorker

data = Queue(maxsize=1)

process = HandTrackingWorker(cv2.VideoCapture(0), data)
process.start()

server = ServerWorker(data)
server.start()
