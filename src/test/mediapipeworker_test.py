from queue import Queue

from src.app.threads import MediapipeWorker
import cv2

data = Queue(maxsize=1)

process = MediapipeWorker(cap=cv2.VideoCapture(0), queue=data, show_image=True)

process.start()
