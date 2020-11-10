import time
import zmq

import cv2
import numpy as np

from minimalhand.wrappers import ModelPipeline

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
cap = cv2.VideoCapture(1)

while True:

    print("Waiting request ...")

    #  Wait for next request from client
    message = socket.recv_string()

    print("Received request: %s" % message)

    if not (message == "handtracking"):
        socket.send(b"error1")
        continue

    ret, frame = cap.read()

    if frame is None:
        socket.send(b"error2")
        continue

    xyz, theta = model.process(handling_frame(frame))

    if xyz is None:
        socket.send(b"error3")
        continue

    n_joint, n_coord = xyz.shape

    if n_joint != 21 or n_coord != 3:
        socket.send(b"error4")
        continue

    socket.send(b"ack")

    for joint in xyz:

        message = socket.recv_string()

        if not (message == "next"):
            socket.send(b"error5")
            break
        socket.send_string("joint;{};{};{}".format(joint[0], joint[1], joint[2]))

    message = socket.recv_string()
    socket.send(b"end")
