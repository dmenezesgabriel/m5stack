"""
This module should be at root dir of esp32 so it can be imported in any file of
app dir if using UIflow firmware from M5Burner.
"""

import socket


class SocketComm:
    def __init__(
        self,
        socket_family,
        socket_type,
        host,
        port,
        backlog,
        buf_size,
    ):
        self.socket_family = socket_family
        self.socket_type = socket_type
        self.host = host
        self.port = port
        self.backlog = backlog
        self.buf_size = buf_size
        self.server_socket = socket.socket(
            self.socket_family, self.socket_type
        )

    def read_comm(self):
        try:
            response = self.client_socket.recv(self.buf_size)
            if len(response):
                response_str = response.decode()
                return response_str
        except Exception as error:
            print("read_comm Error: " + str(error))

    def send_comm(self, payload):
        try:
            self.client_socket.send(payload.encode())
        except Exception as error:
            print("send_comm Error: " + str(error))


class SocketServer(SocketComm):
    def __init__(
        self,
        socket_family,
        socket_type,
        host,
        port,
        backlog,
        buf_size,
    ):
        super().__init__(
            socket_family,
            socket_type,
            host,
            port,
            backlog,
            buf_size,
        )
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.backlog)

    def listen(self, callback):
        """
        listen to client and send a callback.
        """
        while True:
            self.client_socket, address = self.server_socket.accept()
            response_comm = self.read_comm()
            print("Server received: \n", response_comm)
            callback(self, response_comm)
        self.client_socket.close()


class SocketClient(SocketComm):
    def __init__(
        self,
        socket_family,
        socket_type,
        host,
        port,
        backlog,
        buf_size,
    ):
        super().__init__(
            socket_family,
            socket_type,
            host,
            port,
            backlog,
            buf_size,
        )
        self.server_socket.connect((self.host, self.port))

    def start(self, callback):
        """
        Loop and do fn()
        """
        while True:
            callback(self)
        self.server_socket.close()
