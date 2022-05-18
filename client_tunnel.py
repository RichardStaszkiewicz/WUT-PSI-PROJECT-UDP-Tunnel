"""
Project Tag: UTunnel
Project Full Name: Tunnel UDP
Author: Richard Staszkiewicz, Katarzyna Glaza, Krystian Kamiński, Michał Bielak
Last modified: 6.12.2020
all rights reserved
"""

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

    :param Thost: User-Provided. TCP Host parameters to be provided by client.
    :type Thost: Host

    :param Uhost: User-Provided. UDP Host parameters client forwards messages.
    :type Uhost: Host

    Creates client side of TCP-Tunnel implemented during project.
    Used to recieve TCP communication and send UDP messages containing it
    via tunnel.
    """
    def __init__(self, Thost: Host, Uhost: Host, Interactive=True) -> None:
        self.Thost = Thost
        self.Uhost = Uhost
        self.interactive = True

    def initiate_connection(self):
        """
        Method initiate_connection. Atributes: None.

        Initiates a connection based on stored host informations.
        Creates a TCP socket listening based on Thost
        Creates a UDP socket for sending datagrams to Uhost
        """
        self.TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TCPsock.bind((self.Thost.IP, self.Thost.port))
        self.TCPsock.listen(6)

        self.UDPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.UDPsock.bind((self.Uhost.IP, self.Uhost.port))

    def send_test_message(self):
        for i in range(0, 5):
            self.TCPsock.sendall(f"Message {i}".encode('utf-8'))
            response = self.TCPsock.recv(BUFSIZE)
            print(str(response.decode('utf-8')))

    def __del__(self):
        self.TCPsock.close()


help(Client)
# c = client(sys.argv[1],int(sys.argv[2]))
