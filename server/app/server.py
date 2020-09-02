import time
import zmq

import cv2
import numpy as np

from app.minimalhand.wrappers import ModelPipeline

################################################################################


def handling_frame(frame):
    if frame.shape[0] > frame.shape[1]:
        margin = int((frame.shape[0] - frame.shape[1]) / 2)
        frame = frame[margin:-margin]
    else:
        margin = int((frame.shape[1] - frame.shape[0]) / 2)
        frame = frame[:, margin:-margin]

    frame = np.flip(frame, axis=1).copy()
    return cv2.resize(frame, (128, 128))


################################################################################
#   Creatig server and socket binding
################################################################################
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

################################################################################
#   Starting Hand-tracking
################################################################################
model = ModelPipeline()

################################################################################
#   Starting WebCam
################################################################################
cap = cv2.VideoCapture(0)

while True:

    print("start")

    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)

    time.sleep(0.1)

    ret, frame = cap.read()

    #  Send reply back to client
    #  In the real world usage, after you finish your work, send your output here
    socket.send(b"World")
    if frame is not None:
        result_3d, _ = model.process(handling_frame(frame))
        print(result_3d)
        # TODO send joints
