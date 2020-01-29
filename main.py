from config import config
from classes.SockerServer import SocketServer

if __name__ == '__main__':
    SocketServer(config).start()
