import zmq
import time

context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

current_time = time.time()
num_requests = 0
num_requests_with_data = 0

while True:
    socket.send_string("handtracking")
    message = socket.recv_json()
    final_time = time.time() * 1000

    if message.get("metrics") is not None:
        x = message["metrics"]["start_time"]
        webcam_duration = message["metrics"]["capture"]
        mediapipe_duration = message["metrics"]["mediapipe"]
        process_duration = message["metrics"]["duration"]
        queue_duration = message["metrics"]["server"] - message["metrics"]["end_time"]
        read_duration = final_time - message["metrics"]["server"]
        total_duration = final_time - message["metrics"]["start_time"]

        print(x, webcam_duration, mediapipe_duration, process_duration, queue_duration, read_duration, total_duration)
