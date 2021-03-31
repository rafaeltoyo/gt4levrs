import time
import zmq

import cv2
import numpy as np


def jeferson(array, fn=None):
    return '[' + ','.join((x if fn is None else fn(x)) for x in array) + ']'


################################################################################
#   Creatig src and socket binding
################################################################################
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

data = np.array([[1, 1, 1], [2, 1, 1]], dtype="float")

while True:

    print("start")

    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)

    time.sleep(1)

    #  Send reply back to client
    #  In the real world usage, after you finish your work, send your output here
    socket.send_string(jeferson(data, fn=lambda x: jeferson(x, fn=lambda y: str(y))))
