import threading
import time
from queue import Queue
import mediapipe.python.solutions.hands as mp_hands
import cv2

from src.app.mediapipeutils import MediapipeResultParser


class MediapipeThreadingQueue(threading.Thread):
    def __init__(self, *args, **kwargs):
        self.queue = Queue()
        self.cap = cv2.VideoCapture(0)
        self.hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mediapipe_parser = MediapipeResultParser()
        super().__init__(*args, **kwargs)

    def start_thread_debug(self):
        self.working_thread = threading.Thread(target=self.mediapipe_worker_debug)
        self.working_thread.start()

    def start_thread(self):
        self.working_thread = threading.Thread(target=self.mediapipe_worker)
        self.working_thread.start()

    def release(self):
        self.cap.release()

    def mediapipe_worker_debug(self):
        while True:
            ########################################
            # Stage 03 - Capture frame from cam
            print("Getting image  ......{thread}".format(thread=threading.get_ident()))
            success, image = self.cap.read()

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            print("Converting image {shape}......{thread}".format(thread=threading.get_ident(), shape=image.shape))
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

            ########################################
            # Stage 04 - Call mediapipe
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            print("Processing image {shape}......{thread}".format(thread=threading.get_ident(), shape=image.shape))
            results = self.hands.process(image)
            if results.multi_handedness is None:
                continue

            print("Parsing results {results}......{thread}".format(thread=threading.get_ident(), results=results))
            mediapipe_parsed_result = self.mediapipe_parser.parse(results)

            if self.queue.qsize() > 4:
                self.queue.get()

            print("Saving result......{thread}".format(thread=threading.get_ident()))
            self.queue.put((image, mediapipe_parsed_result))

    def mediapipe_worker(self):
        while True:
            ########################################
            # Stage 03 - Capture frame from cam
            success, image = self.cap.read()

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

            ########################################
            # Stage 04 - Call mediapipe
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = self.hands.process(image)
            if results.multi_handedness is None:
                continue

            mediapipe_parsed_result = self.mediapipe_parser.parse(results)

            if self.queue.qsize() > 4:
                self.queue.get()

            self.queue.put((image, mediapipe_parsed_result))

    def get_results(self):
        print("Getting result......{thread}".format(thread=threading.get_ident()))
        image, results = self.queue.get()
        return image, results


if __name__ == "__main__":
    mediapipe_queue = MediapipeThreadingQueue()

    mediapipe_queue.start_thread()

    while True:
        result = mediapipe_queue.get_results()
        print("--------------- Getting result ---------------" + result)


