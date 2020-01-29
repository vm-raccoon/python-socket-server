import socket
from threading import Thread
from classes.SocketClient import SocketClient
from classes.SocketHandler import SocketHandler


class SocketServer:
    def __init__(self, config=None):
        self._setConfigParams(config)
        self.server = None
        self.client_id = 0

    def _setConfigParams(self, config):
        defaults = config is None
        self.host = config['host'] if not defaults else '127.0.0.1'
        self.port = config['port'] if not defaults else 10101
        self.max_connections = config['max_connections'] if not defaults else 10

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        self.server.bind((self.host, self.port))
        self.server.listen(self.max_connections)
        while True:
            _socket, _address = self.server.accept()
            self.client_id += 1
            client = SocketClient(_socket, _address, self.client_id)
            print(f'[{client.ip}:{client.port}] connected')
            SocketHandler(client).start()
