import socket
import sys
import time
import threading
import os
from config import config

def run_server(config):
    serv_sock = create_serv_sock(config['server'], config['port'])
    cid = 0
    while True:
        client_sock = accept_client_conn(serv_sock, cid)
        t = threading.Thread(target=serve_client, args=(client_sock, cid, config))
        t.start()
        cid += 1

def serve_client(client_sock, cid, config):
    try:
        while True:
            request = read_request(client_sock)
            if request is None:
                print(f'Client #{cid} unexpectedly disconnected')
                break
            else:
                #print(f'Client #{cid} get: %s' % request.decode().strip())
                print('Client #{cid} get %s' % request)
                response = handle_request(request)
                #peername = client_sock.getpeername()
                #cmd = request.decode().strip() + ';ip=%s;port=%s;' % peername
                #cmd = '%s "%s" > /dev/null 2>&1' % (config['artisan_cmd'], cmd)
                #os.system(cmd)
                write_response(client_sock, response, cid)
    except ConnectionResetError:
        return None
    except:
        raise

def create_serv_sock(server, port):
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
    serv_sock.bind((server, port))
    serv_sock.listen(1)
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

def handle_request(request):
    #time.sleep(5)
    return request

def write_response(client_sock, response, cid):
    client_sock.sendall(response)
    #client_sock.close()
    #print(f'Client #{cid} has been served')


if __name__ == '__main__':
    run_server(config)











# import socket
# import sys
#
# sock = socket.socket(socket.af_inet, socket.sock_stream)
#
# server_address = ('localhost', 10101)
# print('starting up on %s port %s' % server_address)
# sock.bind(server_address)
#
# sock.listen(1)
#
# while true:
#         print('waiting for a connection')
#         connection, client_address = sock.accept()
#         if connection:
#                 try:
#                         print('connection from', client_address)
#                         while true:
#                                 data = connection.recv(1024)
#                                 print('received "%s"' % data)
#                                 if data:
#                                         print('sending data back to the client')
#                                         connection.sendall(data)
#                                 else:
#                                         print('no more data from', client_address)
#                                         break
#                 finally:
#                         connection.close()
