import time
import socket
import select
import threading
from settings import BUFFER_SIZE

class Client(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(2)
        self.socket_list = [self.sock]

        try:
            self.sock.connect((host, port))
            self.running = True
        except:
            self.failed_to_connect()
            self.running = False

    def run(self):
        while self.running:
            sread, swrite, serror = select.select(self.socket_list, self.socket_list, [], 0)

            for read_socket in sread:
                if read_socket == self.sock:
                    try:
                        data = read_socket.recv(BUFFER_SIZE)
                        if data:
                            self.recieving(data)
                        else:
                            self.lost_connection()
                            self.running = False
                    except:
                        self.lost_connection()

            for write_socket in swrite:
                self.sending(write_socket)

            time.sleep(0.04)

        self.sock.close()

    def recieving(self, data):
        pass

    def sending(self, socket):
        pass

    def lost_connection(self):
        pass

    def failed_to_connect(self):
        pass
