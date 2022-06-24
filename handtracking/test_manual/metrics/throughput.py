import zmq
import time

########################################

NUM_REQUEST = 60_000
CHECKPOINT = 1_000

########################################

old_checkpoint = 0
new_checkpoint = 0

num_requests = 0
num_requests_with_data = 0

num_total_requests = 0
num_total_requests_with_data = 0

########################################

context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

########################################

start_time = time.time()

while num_total_requests < NUM_REQUEST:

    # Handshake
    socket.send_string("handtracking")
    # Request
    message = socket.recv_json() or {}

    # Count request
    num_requests += 1
    num_total_requests += 1
    if message.get("metrics") is not None:
        num_requests_with_data += 1
        num_total_requests_with_data += 1

    # Update checkpoint
    if num_requests > CHECKPOINT:
        old_checkpoint = new_checkpoint
        new_checkpoint = time.time()

        duration = new_checkpoint - old_checkpoint

        print("%s req/s [all]" % (num_requests / duration))
        print("%s req/s [data]" % (num_requests_with_data / duration))

        num_requests = 0
        num_requests_with_data = 0

duration = time.time() - start_time

print("END!")
print("%s req/s [all]" % (num_total_requests / duration))
print("%s req/s [data]" % (num_total_requests_with_data / duration))
