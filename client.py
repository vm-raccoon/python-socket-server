import socket
import threading
from config import config


def run_socket(index, _config):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (_config['server'], _config['port'])
    print(f'{index} connecting to %s port %s' % server_address)
    sock.connect(server_address)
    try:
        for i in range(0, 10): # * random.randint(1, 5)):
            message = '1234567\n'.encode()
            print(f'{index} sending "%s"' % message)
            sock.sendall(message)
            amount_received = 0
            amount_expected = len(message)
            data = None
            while amount_received < amount_expected:
                data = sock.recv(8)
                amount_received += len(data)
            print(f'{index} received "%s"' % data)
    finally:
        print(f'{index} closing socket')
        sock.close()


for k in range(0, 1):
    threading.Thread(target=run_socket, args=(k, config,)).start()
