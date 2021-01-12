from enum import Enum


class CommunicationState(Enum):
    STATE01 = 1
    STATE02 = 2
    STATE03 = 3


class CommunicationController:

    def __init__(self):
        self.state = CommunicationState.STATE01

    def process(self, data):
        pass

    def process_message(self, message):
        print("Received request: %s" % message)
        pass
