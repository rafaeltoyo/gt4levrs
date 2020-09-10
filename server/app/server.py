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


def jeferson(array, fn=None):
    return '[' + ','.join((x if fn is None else fn(x)) for x in array) + ']'


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

    result_3d, _ = model.process(handling_frame(frame))

    if result_3d is None:
        socket.send(b"error3")
        continue

    n_joint, n_coord = result_3d.shape

    if n_joint != 21 or n_coord != 3:
        socket.send(b"error4")
        continue

    socket.send(b"ack")

    for joint in result_3d:

        message = socket.recv_string()

        if not (message == "next"):
            socket.send(b"error5")
            break
        socket.send_string("joint;{};{};{}".format(joint[0], joint[1], joint[2]))

    message = socket.recv_string()
    socket.send(b"end")
