import cv2
import numpy as np
from minimalhand.wrappers import ModelPipeline, ModelDet
from minimalhand.mano import plot_hand

modelpp = ModelPipeline()

from src.app.handtracking.yolo import YOLO

yolo_model = YOLO.get_yolo_object(network="prn", confidence=0.3)

cap = cv2.VideoCapture(0)

while 1:
    ret, frame_large = cap.read()

    if frame_large is None:
        continue

    if frame_large.shape[0] > frame_large.shape[1]:
        margin = int((frame_large.shape[0] - frame_large.shape[1]) / 2)
        frame_large = frame_large[margin:-margin]
    else:
        margin = int((frame_large.shape[1] - frame_large.shape[0]) / 2)
        frame_large = frame_large[:, margin:-margin]

    frame_large = np.flip(frame_large, axis=1).copy()

    iw, ih, inference_time, results = yolo_model.inference(frame_large)
    output_frame = frame_large.copy()

    if len(results) == 2:
        _, _, _, x1, y1, _, _ = results[0]
        _, _, _, x2, y2, _, _ = results[1]

        if x1 < x2:
            left_hand = 0
        else:
            left_hand = 1
    left_hand = -1

    for index in range(len(results)):
        id, name, confidence, x1, y1, w, h = results[index]
        x2 = x1 + w
        y2 = y1 + h

        YOLO.print_hand_detection(output_frame, x1, y1, w, h, confidence, name)

        adjusted_y1 = int(y1 * 0.8)
        adjusted_y2 = int(y2 * 1.15)
        adjusted_x1 = int(x1 * 0.8)
        adjusted_x2 = int(x2 * 1.15)
        hand_frame = frame_large[adjusted_y1: adjusted_y2, adjusted_x1: adjusted_x2]

        hand_frame = cv2.resize(hand_frame, (128, 128))

        if index == left_hand:
            hand_frame = cv2.flip(hand_frame, 1)

        result_3d, heatmap = modelpp.process(hand_frame)

        ################################################################################
        #   Ploting results
        ################################################################################

        fixed_heatmap = (result_3d/2 + 1) * 200

        handimg = np.ones(shape=(300, 300, 3), dtype='uint8') * 255
        plot_hand(fixed_heatmap, None, img=handimg)

        cv2.imshow('hand_frame', hand_frame)
        cv2.imshow('heatmap', handimg)

        ################################################################################
        #   Printing results
        ################################################################################

        print(result_3d)

        print(result_3d.shape)

    cv2.imshow('frame_large', frame_large)
    cv2.waitKey(1)
