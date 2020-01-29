class SocketClient:
    def __init__(self, _socket, _address, _id):
        self.socket = _socket
        self.ip = _address[0]
        self.port = _address[1]
        self.id = _id
