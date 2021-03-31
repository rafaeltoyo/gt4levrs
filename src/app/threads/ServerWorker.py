from threading import Thread
from queue import Queue, Empty

import zmq

HANDSHAKE = "handtracking"
ADDRESS = "tcp://*:5555"


class ServerConnection:

    _socket: zmq.Socket = None

    def __init__(self):
        """ Server connection handler """
        pass

    def setup(self, address: str):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind(address)
        self._socket = socket

    def read_string(self):
        return self._socket.recv_string()

    def send_string(self, message: str):
        self._socket.send_string(message)

    def send_json(self, json: object):
        self._socket.send_json(json)


class ServerWorker(Thread):

    def __init__(self, queue: Queue):
        """
        Server worker.
        Define and setup the server configuration.
        Parameters
        ----------
        queue Queue with data from handtracking system
        """
        self.conn: ServerConnection = ServerConnection()
        self.queue: Queue = queue

        super().__init__(
            target=self._behaviour,
            name="Server worker",
            daemon=True)

    def _behaviour(self):
        """
        Worker behaviour.
        This function gonna be the Thread target
        """
        self.conn.setup(ADDRESS)

        while self.is_alive():

            message = self.conn.read_string()

            if message == HANDSHAKE:
                try:
                    data = self.queue.get_nowait()
                    self.conn.send_json(data)
                except Empty:
                    self.conn.send_json({})
                except Exception as ex:
                    self.conn.send_json(ex)

            else:
                pass

        print("Stopping Server Worker!")
