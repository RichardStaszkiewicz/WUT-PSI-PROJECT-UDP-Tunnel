"""
Project Tag: UTunnel
Project Full Name: Tunnel UDP
Author:
Last modified: 6.12.2020
all rights reserved
"""

import sys
import socket

BUFSIZE = 512
# python3 client.py 192.168.1.19 9990

class Host(object):
    def __init__(self, IP, port) -> None:
        self.IP = IP
        self.port = port

class Client(object):
    """
    Class client. Atributes:

    :param Thost: User-Provided. Server IP on the tunnel end.
    :type Thost: str

    :param Uhost: User-Provided. Server IP on the tunnel end.
    :type Uhost: float

    Creates client side of TCP-Tunnel implemented during project.
    Used to recieve TCP communication and send UDP messages containing it
    via tunnel.
    """
    def __init__(self, Thost : Host, Uhost : Host):
        self.Thost = Thost
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((Thost.IP, Thost.port))

    def send_test_message(self):
        for i in range(0,5):
            self.sock.sendall(f"Message {i}".encode('utf-8'))
            response = self.sock.recv(BUFSIZE)
            print(str(response.decode('utf-8')))

    def __del__(self):
        self.sock.close()

help(Client)
## c = client(sys.argv[1],int(sys.argv[2]))
