#rcon handler for cod4 server

import socket

class cod4server:
    def __init__(self, ip, port, password):
        self.server = (ip, port)
        self.password = password
        self.conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def send(self, command):
        header = b'\xff\xff\xff\xffrcon '
        self.conn.sendto(header + str.encode(self.password) + str.encode(f" {command}"),self.server )
    
    def recieve(self):
        # returns the string read from the socket used
        return self.conn.recvfrom(1024)[0]


