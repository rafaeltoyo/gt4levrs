import time
import threading
from queue import Queue, Empty
import zmq
from zmq import ZMQError

from ..config import ServerConfig as Config

import logging
from ..utils.logging_manager import LoggingManager


class ServerConnection:
    _socket: zmq.Socket = None

    def setup(self, address: str):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind(address)
        self._socket = socket

    def read_string(self) -> str:
        try:
            return self._socket.recv_string()
        except Exception as ex:
            return self._socket.recv()

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
                 handshake: str = Config.handshake,
                 debug_metrics: bool = False):
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

        self.debug_metrics = debug_metrics

        self.logger = LoggingManager.get_logger("HandtrackingWorkers", logging_level=logging.INFO)

    def run(self):
        self.conn.setup(self._address)

        self.logger.info("Starting Server Worker!")

        while self.is_alive():
            try:
                message = self.conn.read_string()
            except Exception as ex:
                self.logger.error(ex)
                continue

            if message == self._handshake:
                try:
                    data = self.queue.get_nowait()
                    if self.debug_metrics:
                        data["metrics"]["server"] = time.time() * 1000
                    self.logger.info("Sending %s!", str(data))
                    self.conn.send_json(data)
                except Empty:
                    self.conn.send_json({})
                except Exception as ex:
                    self.conn.send_json({'error': str(ex)})
            else:
                pass

        self.logger.info("Stopping Server Worker!")
