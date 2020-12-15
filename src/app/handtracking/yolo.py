import time

import cv2
import numpy as np

from src.app.file_utils import get_absolute_path


class YOLO:
    @staticmethod
    def get_yolo_object(network, confidence=0.5):
        if network == "normal":
            print("loading yolo...")
            cross_hands_path = get_absolute_path("src/app/handtracking/models/cross-hands.cfg")
            model_path = get_absolute_path("src/app/handtracking/models/cross-hands.weights")
            yolo = YOLO(cross_hands_path, model_path, ["hand"], confidence=confidence)
        elif network == "prn":
            print("loading yolo-tiny-prn...")
            cross_hands_path = get_absolute_path("src/app/handtracking/models/cross-hands-tiny-prn.cfg")
            model_path = get_absolute_path("src/app/handtracking/models/cross-hands-tiny-prn.weights")
            yolo = YOLO(cross_hands_path, model_path, ["hand"], confidence=confidence)
        elif network == "v4-tiny":
            print("loading yolov4-tiny-prn...")
            cross_hands_path = get_absolute_path("src/app/handtracking/models/cross-hands-yolov4-tiny.cfg")
            model_path = get_absolute_path("src/app/handtracking/models/cross-hands-yolov4-tiny.weights")
            yolo = YOLO(cross_hands_path, model_path, ["hand"], confidence=confidence)
        else:
            print("loading yolo-tiny...")
            cross_hands_path = get_absolute_path("src/app/handtracking/models/cross-hands-tiny.cfg")
            model_path = get_absolute_path("src/app/handtracking/models/cross-hands-tiny.weights")
            yolo = YOLO(cross_hands_path, model_path, ["hand"], confidence=confidence)

        return yolo

    def __init__(self, config, model, labels, size=416, confidence=0.5, threshold=0.3):
        self.confidence = confidence
        self.threshold = threshold
        self.size = size

        self.labels = labels
        try:
            self.net = cv2.dnn.readNetFromDarknet(config, model)
        except:
            raise ValueError(
                "Couldn't find the models!\nDid you forget to download them manually (and keep in the correct directory, models/) or run the shell script?")

    def inference_from_file(self, file):
        mat = cv2.imread(file)
        return self.inference(mat)

    def inference(self, image):
        ih, iw = image.shape[:2]

        ln = self.net.getLayerNames()
        ln = [ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (self.size, self.size), swapRB=True, crop=False)
        self.net.setInput(blob)
        start = time.time()
        layerOutputs = self.net.forward(ln)
        end = time.time()
        inference_time = end - start

        boxes = []
        confidences = []
        classIDs = []

        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > self.confidence:
                    # scale the bounding box coordinates back relative to the
                    # size of the image, keeping in mind that YOLO actually
                    # returns the center (x, y)-coordinates of the bounding
                    # box followed by the boxes' width and height
                    box = detection[0:4] * np.array([iw, ih, iw, ih])
                    (centerX, centerY, width, height) = box.astype("int")
                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence, self.threshold)

        results = []
        if len(idxs) > 0:
            for i in idxs.flatten():
                # extract the bounding box coordinates
                x, y = (boxes[i][0], boxes[i][1])
                w, h = (boxes[i][2], boxes[i][3])
                id = classIDs[i]
                confidence = confidences[i]

                results.append((id, self.labels[id], confidence, x, y, w, h))

        return iw, ih, inference_time, results

    @staticmethod
    def print_hand_detection(frame, x1, y1, w, h, confidence, name):
        # draw a bounding box rectangle and label on the image
        color = (0, 255, 255)
        cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), color, 2)
        text = "%s (%s)" % (name, round(confidence, 2))
        cv2.putText(frame, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        return frame
