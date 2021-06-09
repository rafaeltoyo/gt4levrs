from queue import Queue

import cv2

from app.threads import ServerWorker, MediapipeWorker

data = Queue(maxsize=1)

process = MediapipeWorker(cv2.VideoCapture(0), data)
process.start()

server = ServerWorker(data)
server.start()
