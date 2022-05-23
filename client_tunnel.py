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
    except Exception:
        raise EnvironmentError


class SendingSocketUDP(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(),
                 kwargs=None, verbose=None) -> None:
        super(SendingSocketUDP, self).__init__()
        self.target = target
        self.name = name

    def run(self):
        logging.debug(f"Initiating UDP sending Socket...")
        pass


class RecievingSocketUDP(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(),
                 kwargs=None, verbose=None) -> None:
        super(RecievingSocketUDP, self).__init__()
        self.target = target
        self.name = name

    def run(self):
        logging.debug(f"Initiating UDP recieving Socket...")
        pass


class SocketTCP(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(),
                 kwargs=None, verbose=None) -> None:
        super(SocketTCP, self).__init__()
        self.target = target
        self.name = name

    def run(self):
        logging.debug(f"Initiating TCP Socket...")
        pass


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
        sys.exit(1)
    except ConfigFileInvalid:
        print(f"Configuration file {sys.argv[1]} format corrupt!")
        exit(1)
    except EnvironmentError:
        print(f"Unsupported by environment operation.")
        print(f"Have you set up the environment approprietly?")
        exit(1)

    print(CONFIG)
