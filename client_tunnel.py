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

class PortNumberException(Exception):
    """
    Exception PortNumberException. Atributes None.
    Thrown in case of port number being corrupt.
    """
    pass

class Host(object):
    """
    Class Host. Atributes:
    :param IP: Host IP
    :type IP: str

    :param port: Host port in range of (0, 65535)
    :type port: str

    class stores information about the host.
    """
    def __init__(self, IP, port):
        self.IP = IP
        self.port = port
        try:
            if int(port) > 65535:
                raise Exception()
        except Exception:
            raise PortNumberException("too big port")

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
    def __init__(self, Thost: Host, Uhost: Host) -> None:
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
