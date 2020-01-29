from threading import Thread


class SocketHandler(Thread):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        try:
            while True:
                request = self.read_request()
                if request is None:
                    print(f'[{self.client.ip}:{self.client.port}] disconnected')
                    break
                else:
                    print(f'[{self.client.ip}:{self.client.port}] get: %s' % request.decode().strip())
                    response = b"Response: "
                    response += request
                    self.client.socket.sendall(response)
        except ConnectionResetError:
            return None
        except:
            raise

    def read_request(self, delimiter=b'\n'):
        request = bytearray()
        try:
            while True:
                chunk = self.client.socket.recv(1)
                if not chunk:
                    return None
                request += chunk
                if delimiter in request:
                    return request
        except ConnectionResetError:
            return None
        except:
            raise
