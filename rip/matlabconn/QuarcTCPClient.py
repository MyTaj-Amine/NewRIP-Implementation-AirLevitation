import socket
import struct
import time


class QuarcTCPClient(object):

    def __init__(self, port):
        self.server_address = (socket.gethostbyname(socket.gethostname()), port)
        self.sock = None
        while self.sock is None:
            self.sock = socket.create_connection(self.server_address)
            time.sleep(0.5)
        self.num_bytes = 0
        self.code = []

    def config(self, types):
        for type in types:
            if type == "double" or type == "float" or type == "integer":
                    self.code.append('d')
                    self.num_bytes += 8
            # TODO: Add support for other types

    def read(self, variables):
        data = {}
        i = 0
        sock_data = self.sock.recv(self.num_bytes)
        for name in variables:
            self.s = struct.Struct('<' + self.code[i])  # '<' for little endian byte ordering
            data[name] = self.s.unpack_from(sock_data, i*8)[0]  # TODO: Add support for other types
            i += 1
        return data

    def close(self):
        self.sock.close()
