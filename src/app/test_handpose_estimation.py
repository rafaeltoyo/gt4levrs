import cv2
import numpy as np
import app.minimalhand.config as config
from app.minimalhand.wrappers import ModelPipeline, ModelDet
from app.minimalhand.mano import plot_hand

# model = ModelDet(config.DETECTION_MODEL_PATH)
modelpp = ModelPipeline()

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
    frame = cv2.resize(frame_large, (128, 128))

    result_3d, heatmap = modelpp.process(frame)

    ################################################################################
    #   Ploting results
    ################################################################################

    fixed_heatmap = (result_3d/2 + 1) * 200

    handimg = np.ones(shape=(300, 300, 3), dtype='uint8') * 255
    plot_hand(fixed_heatmap, None, img=handimg)

    cv2.imshow('webcam', frame_large)
    cv2.imshow('heatmap', handimg)

    cv2.waitKey(50)

    ################################################################################
    #   Printing results
    ################################################################################

    print(result_3d)

    print(result_3d.shape)
