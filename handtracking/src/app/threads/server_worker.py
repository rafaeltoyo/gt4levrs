import multiprocessing
import threading
from queue import Queue, Empty
import zmq
from ..config import ServerConfig as Config


class ServerConnection:
    _socket: zmq.Socket = None

    def setup(self, address: str):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind(address)
        self._socket = socket

    def read_string(self) -> str:
        return self._socket.recv_string()

    def send_string(self, message: str):
        self._socket.send_string(message)

    def send_json(self, json: object):
        self._socket.send_json(json)


class ServerWorker(threading.Thread):

    def __init__(self,
                 queue: Queue,
                 address: str = Config.address,
                 port: int = Config.port,
                 protocol: str = Config.protocol,
                 handshake: str = Config.handshake):
        """
        Server worker.
        Define and setup the server configuration.

        Parameters
        ----------
        queue
            Queue with data from handtracking system
        address
            Server address. Default value is * (localhost).
        port
            Server port. Default value is 5555.
        protocol
            Server protocol. Default value is TCP.
        handshake
            Handshake string.
        """
        threading.Thread.__init__(self)
        self.conn: ServerConnection = ServerConnection()
        self.queue: Queue = queue
        self._address = "{}://{}:{}".format(protocol, address, port)
        self._handshake = handshake

    def run(self):
        self.conn.setup(self._address)

        while self.is_alive():
            message = self.conn.read_string()
            if message == self._handshake:
                try:
                    data = self.queue.get_nowait()
                    print("Sending data " + str(data))
                    self.conn.send_json(data)
                except Empty:
                    self.conn.send_json({})
                except Exception as ex:
                    self.conn.send_json(ex)
            else:
                pass

        print("Stopping Server Worker!")
