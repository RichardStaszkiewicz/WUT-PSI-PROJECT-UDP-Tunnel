import sys
import socket

BUFSIZE = 512
# python3 client.py 192.168.1.19 9990

class client:
    def __init__(self, sHOST,sPORT):
        self.sHOST = sHOST
        self.sPORT = sPORT
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((sHOST,sPORT))

    def send_test_message(self):
        for i in range(0,5):
            self.sock.sendall(f"Message {i}".encode('utf-8'))
            response = self.sock.recv(BUFSIZE)
            print(str(response.decode('utf-8')))

    def __del__(self):
        self.sock.close()

c = client(sys.argv[1],int(sys.argv[2]))
