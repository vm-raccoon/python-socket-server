import socket
import threading
import random
from config import config


def run_socket(index, _config):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (_config['host'], _config['port'])
    print(f'{index} connecting to %s port %s' % server_address)
    sock.connect(server_address)
    try:
        for i in range(0, 100 * random.randint(1, 2)):
            message = '123\n'.encode()
            print(f'{index} sending "%s"' % message)
            sock.sendall(message)
            response = bytearray()
            delimiter = b'\n'
            while True:
                chunk = sock.recv(1)
                if not chunk:
                    break
                response += chunk
                if delimiter in response:
                    break
            print(f'{index} received "%s"' % response.decode().strip())
    finally:
        print(f'{index} closing socket')
        sock.close()


for k in range(0, 100):
    threading.Thread(target=run_socket, args=(k, config,)).start()
