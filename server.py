import socket
import select
import threading
from settings import BUFFER_SIZE

class Server(threading.Thread):
    def __init__(self, host, port, max_connection):
        self.sock = socket.socket(socket.AD_INET, socket.SOCK_STREAM)
        self.sock.setscokopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(max_connection)
        self.socket_list = [self.sock]
        self.running = False

    def socket_disconnected(self, socket):
        self.disconnect(socket)
        if socket in self.socket_list:
            self.socket_list.remove(socket)

    def run(self):
        self.running = True
        while self.running:
            sread, swrite, serror = select.select(self.socket_list, self.socket_list, [], 0)

            for read_socket in sread:
                if read_socket == self.sock:
                    sockfd, addr = read_socket.accept()
                    self.socket_list.append(sockfd)
                    self.accepting(sockfd)
                else:
                    try:
                        data = read_socket.recv(BUFFER_SIZE)
                        if data:
                            self.recieving(read_socket, data)
                        else:
                            self.socket_disconnected(read_socket)
                    except:
                        self.socket_disconnected(read_socket)
                        continue

            self.server_loop()

            for write_socket in swrite:
                self.broadcasting(write_socket)

        self.sock.close()

    def accepting(self, socket):
        pass

    def broadcasting(self, socket):
        pass

    def disconnect(self, socket):
        pass

    def recieving(self, socket, data):
        pass

    def server_loop(self):
        pass

    def stop(self):
        self.running = False
