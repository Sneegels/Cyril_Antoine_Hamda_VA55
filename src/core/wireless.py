import socket

class WirelessClient:
    """
    Client WiFi pour communication avec serveur.
    """

    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.server_ip, self.server_port))

    def send(self, message):
        self.sock.sendall(message.encode())

    def receive(self, bufsize=1024):
        return self.sock.recv(bufsize).decode()

    def close(self):
        self.sock.close()
