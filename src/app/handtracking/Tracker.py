import cv2
import dlib


class Tracker():
    def __init__(self):
        self.track_frames = 10
        self.trackers = []
        self.texts = []

    def reset(self):
        self.trackers = []
        self.texts = []

    def track_non_result_frame(self, frame):
        for tracker, text in zip(self.trackers, self.texts):
            pos = tracker.get_position()

            # unpack the position object
            startX = int(pos.left())
            startY = int(pos.top())
            endX = int(pos.right())
            endY = int(pos.bottom())

            cv2.rectangle(frame, (startX, startY), (endX, endY), (255, 0, 0), 2)
            cv2.putText(frame, text, (startX, startY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    def track_result_frame(self, name, rgb, bbox):
        x, y, w, h = bbox[0], bbox[0], bbox[0], bbox[0]
        tracker = dlib.correlation_tracker()

        # left, top, right, bottom
        rect = dlib.rectangle(x, y, w, h)
        tracker.start_track(rgb, rect)
        self.trackers.append(tracker)
        self.texts.append(name)
