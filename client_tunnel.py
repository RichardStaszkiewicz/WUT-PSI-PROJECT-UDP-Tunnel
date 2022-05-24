"""
Project Tag: UTunnel
Project Full Name: Tunnel UDP
Author: Richard Staszkiewicz, Katarzyna Glaza, Krystian Kamiński, Michał Bielak
Last modified: 23.05.2022
all rights reserved
"""

import socket
import json
import sys
import logging
import queue
import threading
import time

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

#  GROUND TRUTHS ###########
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)
END_PROGRAM = False
# TCP_SEND = None     # A Queue of messages to be send via TCP socket
# UDP_SEND = None     # A Queue of messages to be send via UDP socket
# CONFIG = None       # A Dict of configurations specific to the run


BUFSIZE = 512


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


class EnvironmentError(Exception):
    """
    Exception EnvironmentError. No atributes.
    Raises when user has environment not compatible with the program.
    """
    pass


def env_setup():
    """
    Function env_setup. No Arguments.
    :return: configuration as dict

    Verifies the configuration legitimacy, sets up working environment.
    """
    if len(sys.argv) != 2:
        raise ZeroDivisionError

    try:
        with open(sys.argv[1], "r+") as handle:
            global CONFIG
            CONFIG = json.load(handle)
    except Exception:
        raise ConfigFileInvalid

    try:
        global TCP_SEND
        TCP_SEND = queue.Queue(int(CONFIG["TCP Buffer Size"]))
        global UDP_SEND
        UDP_SEND = queue.Queue(int(CONFIG["TCP Buffer Size"]))
    except Exception:
        raise EnvironmentError


class SendingSocketUDP(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(),
                 kwargs=None, verbose=None) -> None:
        super(SendingSocketUDP, self).__init__()
        self.target = target
        self.name = name

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host_ip = CONFIG["Host IP"]
        port = int(CONFIG["UDP Client Port"])
        info = f"Opening Socket on {host_ip}:{port}"
        logging.debug(info)

        self.socket.bind((host_ip, port))

        stamp = (CONFIG["Send UDP to IP"], CONFIG["Send UDP to Port"])
        info = f"Socket sending to {stamp[0]}:{stamp[1]}"
        logging.debug(info)

        while not END_PROGRAM:
            if not UDP_SEND.empty():
                item = UDP_SEND.get()
                self.socket.sendto(item, stamp)
            else:
                time.sleep(1)

        logging.debug(f"Closing Socket...")
        self.socket.close()
        return


class RecievingSocketUDP(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(),
                 kwargs=None, verbose=None) -> None:
        super(RecievingSocketUDP, self).__init__()
        self.target = target
        self.name = name

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(0.5)

        host_ip = CONFIG["Host IP"]
        port = int(CONFIG["UDP Server Port"])
        info = f"Opening Socket on {host_ip}:{port}"
        logging.debug(info)

        self.socket.bind((host_ip, port))
        buf = int(CONFIG["UDP Buffer Size"])

        while not END_PROGRAM:
            try:
                data, address = self.socket.recvfrom(buf)
            except socket.timeout:
                data = None
            if data:
                logging.debug(f"Recieved {len(data)}B from {address}")
                TCP_SEND.put(data)

        logging.debug(f"Closing Socket...")
        self.socket.close()
        return


class SocketTCP(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(),
                 kwargs=None, verbose=None) -> None:
        super(SocketTCP, self).__init__()
        self.target = target
        self.name = name

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)
        self.bufsize = CONFIG["TCP Buffer Size"]
        host_ip = CONFIG["Host IP"]
        port = int(CONFIG["TCP Port"])
        info = f"Opening Socket on {host_ip}:{port}"
        logging.debug(info)

        isClient = int(CONFIG["TCP Is Listen"])
        if isClient == 1:
            self.socket.bind((host_ip, port))
            self.server_mode()
        else:
            self.clinet_mode()

        self.socket.close()

    def server_mode(self):
        backlog = int(CONFIG["TCP Backlog"])
        self.socket.listen(backlog)
        logging.debug(f"Socket Listening with {backlog} backlog")

        while not END_PROGRAM:
            connection, addr = self.socket.accept()
            with connection:
                logging.debug(f"Connection accepted from {addr}")
                while not END_PROGRAM:
                    try:
                        message = connection.recv(self.bufsize)
                    except socket.timeout:
                        pass
                    if not message:
                        break
                    UDP_SEND.put(message)
                logging.debug(f"Connection closed by client")
        return

    def clinet_mode(self):
        server_ip = CONFIG["Send TCP to IP"]
        server_port = int(CONFIG["Send TCP to Port"])
        logging.debug(f"Connecting Socket to {server_ip}:{server_port}")
        self.socket.connect((server_ip, server_port))
        while not END_PROGRAM:
            if not TCP_SEND.empty():
                item = TCP_SEND.get()
                self.socket.sendall(item)
            else:
                self.socket.sendall("ping")
                time.sleep(1)
        return


if __name__ == "__main__":
    try:
        env_setup()
        UDP_Send = SendingSocketUDP(name='Sending UDP Socket')
        UDP_Recieve = RecievingSocketUDP(name='Recieving UDP Socket')
        TCP_Socket = SocketTCP(name='TCP Connection Socket')

        UDP_Send.start()
        UDP_Recieve.start()
        TCP_Socket.start()

    except ZeroDivisionError:
        print("Invalid amount of args. Did you enclose configuration file?")
    except ConfigFileInvalid:
        print(f"Configuration file {sys.argv[1]} format corrupt!")
    except EnvironmentError:
        print(f"Unsupported by environment operation.")
        print(f"Have you set up the environment approprietly?")
    except Exception:
        print("Unexpected error occured...")

    # print(CONFIG)

    END_PROGRAM = True
