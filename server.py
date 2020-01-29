import socket
import threading
from config import config
from classes.SockerServer import SocketServer


def run_server(config):
    serv_sock = create_serv_sock(config['server'], config['port'], config['max_connections'])
    cid = 0
    while True:
        client_sock = accept_client_conn(serv_sock, cid)
        t = threading.Thread(target=serve_client, args=(client_sock, cid,))
        t.start()
        cid += 1


def serve_client(client_sock, cid):
    try:
        while True:
            request = read_request(client_sock)
            if request is None:
                print(f'Client #{cid} unexpectedly disconnected')
                break
            else:
                print(f'Client #{cid} get %s' % request)
                client_sock.sendall(request)
    except ConnectionResetError:
        return None
    except:
        raise


def create_serv_sock(server, port, max_connections):
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
    serv_sock.bind((server, port))
    serv_sock.listen(max_connections)
    return serv_sock


def accept_client_conn(serv_sock, cid):
    client_sock, client_addr = serv_sock.accept()
    print(f'Client #{cid} connected {client_addr[0]}:{client_addr[1]}')
    return client_sock


def read_request(client_sock, delimiter=b'\n'):
    request = bytearray()
    try:
        while True:
            chunk = client_sock.recv(1)
            if not chunk:
                return None
            request += chunk
            if delimiter in request:
                return request
    except ConnectionResetError:
        return None
    except:
        raise


if __name__ == '__main__':
    run_server(config)
