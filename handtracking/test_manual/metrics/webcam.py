import time
import cv2

cap = cv2.VideoCapture(0)

current_time = time.time()

num_requests = 0
num_requests_with_data = 0

while True:
    ret, img = cap.read()

    if ret:
        num_requests_with_data += 1
    num_requests += 1

    if time.time() - current_time > 1:
        current_time = time.time()
        print("%s frames/s [all]" % num_requests)
        print("%s frames/s [data]" % num_requests_with_data)
        num_requests = 0
        num_requests_with_data = 0
