from threading import Thread
from queue import Queue, Empty

import cv2

from mediapipe.python.solutions.hands import Hands
from app.mediapipeutils import MediapipeResultParser


class HandTrackingHandler:

    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """ Hand tracking handler """
        self.hands = Hands(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def process(self, image) -> object:
        """
        Process a frame that contains a person and return the positions of him hands

        Parameters
        ----------
        image
            Frame from WebCam

        Returns
        -------
            Json with hands joints position
        """
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False

        # Execute the Mediapipe
        results = self.hands.process(image)

        if results.multi_hand_landmarks:
            return MediapipeResultParser().parse(results)
        else:
            return {}


class HandEstimationWorker(Thread):

    def __init__(self, frame: object, handler: HandTrackingHandler, queue: Queue):
        """
        This thread process the frame and put into queue
        The daemon options  is True because this process can be aborted when program stop

        Parameters
        ----------
        frame   Frame from video
        queue   Queue of hands position
        """
        self.handler = handler
        self.queue = queue
        super().__init__(target=self._behaviour, args=(frame,), daemon=True)

    def _behaviour(self, frame):
        results = self.handler.process(frame)
        try:
            self.queue.get_nowait()
        except Empty:
            pass
        finally:
            self.queue.put_nowait(results)


class PoseEstimationWorker(Thread):

    def __init__(self, frame):
        """
        This thread process the frame and extract person position
        The daemon options  is True because this process can be aborted when program stop

        Parameters
        ----------
        frame   Frame from video
        """
        super().__init__(target=self._behaviour, args=(frame,), daemon=True)

    def _behaviour(self, frame):
        pass


class HandTrackingWorker(Thread):

    def __init__(self, cap: cv2.VideoCapture, queue: Queue):
        self.cap = cap
        self.handler = HandTrackingHandler(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.queue = queue

        super().__init__(
            target=self._behaviour,
            name="Server worker")

    def _behaviour(self):

        count = 0

        while self.cap.isOpened() and self.is_alive():

            # Get a new frame from webcam
            success, image = self.cap.read()
            if not success:
                # If loading a video, use 'break' instead of 'continue'.
                continue

            if count % 5 == 0:
                worker = PoseEstimationWorker(image)
                worker.start()
            else:
                results = self.handler.process(image)
                print(results)
                try:
                    self.queue.get_nowait()
                except Empty:
                    pass
                finally:
                    self.queue.put_nowait(results)

            count += 1

        self.cap.release()
        print("Stopping HandTracking Worker!")

    def _process_hands(self):
        pass
