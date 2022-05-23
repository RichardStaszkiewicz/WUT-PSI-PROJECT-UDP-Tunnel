"""
Project Tag: UTunnel
Project Full Name: Tunnel UDP
Author: Richard Staszkiewicz, Katarzyna Glaza, Krystian Kamiński, Michał Bielak
Last modified: 23.05.2022
all rights reserved
"""

import socket
import json


BUFSIZE = 512
# python3 client.py 192.168.1.19 9990

# CONFIG:
# |  Tag                 | Client Description    | Server Description     |
# |:--------------------:|:---------------------:|:----------------------:|
# |  Send to IP          | Tunel Server-End IP   | Web Server IP          |
# |  Send to Port        | Tunel Server-End Port | Web Server Port        |
# |  Response to IP      | _Not applicable_      | Tunel Client-End IP    |
# |  Response to Port    | _Not applicable_      | Tunel Client-End Port  |
# |  TCP Port            | Opened TCP Port No.   | Opened TCP Port No.    |
# |  TCP Buffer Size     | TCP Buffer Size       | TCP Buffer Size        |
# |  TCP Backlog         | Amount of backloged c.| _Not applicable_       |
# |  TCP is listen       | **CONST 1**           | **CONST 0**            |


class PortNumberException(Exception):
    """
    Exception PortNumberException. Atributes None.
    Thrown in case of port number being corrupt.
    """
    pass


class ConfigFileInvalid(Exception):
    """
    Exception ConfigFileInvalid. Atributes None.
    Thrown in case of problems according to configuration file.
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


class Tunnel(object):
    """
    Class Tunnel. Atributes:

    :param config_file: path to configuration file
    :type config_file: str

    :param Interact: interactive logs prompt on terminal
    :type Interact: bool

    Creates tunnel host implemented by project. Specification of
    server or client end is up to config file.
    """
    def __init__(self, config_file: str, Interact=True):
        try:
            with open(config_file, "r+") as handle:
                self.config = json.load(handle)
        except Exception:
            raise ConfigFileInvalid("Configuration file format corrupt!")
        self.interactive = Interact

    def setup_connections(self):
        """
        Method setup_connections. Arguments: None.

        Initiates a connection based on stored host informations.
        Creates a TCP socket. Depending on config, it might be client or server
        Creates a UDP client and server socket based on Config.
        """
        self.TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TCPsock.bind((self.Thost.IP, self.Thost.port))
        self.TCPsock.listen(6)

        self.UDPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.UDPsock.bind((self.Uhost.IP, self.Uhost.port))

    def accept_TCP(self):
        pass

    def send_UDP(self, message):
        """
        Method send_UDP. Arguments:

        :param message: data to be send via UDP to UServer
        :type message: readable buffer

        Method handling sending a UDP datagrams with a given message.
        """
        self.UDPsock.sendto(message, (self.UServer.IP, self.UServer.port))

    def send_test_message(self):
        for i in range(0, 5):
            self.TCPsock.sendall(f"Message {i}".encode('utf-8'))
            response = self.TCPsock.recv(BUFSIZE)
            print(str(response.decode('utf-8')))

    def __del__(self):
        self.TCPsock.close()
        self.UDPsock.close()


help(Tunnel)
# c = client(sys.argv[1],int(sys.argv[2]))
