from sys import argv

from core.server import Server

if __name__ == '__main__':
    serv = Server(argv[1]) if len(argv) > 1 else Server()
    serv.run()
