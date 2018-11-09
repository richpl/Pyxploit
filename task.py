#! /usr/bin/python

"""
Metaclass that specifies the methods that should be provided
by all instantiating classes that are passed as arguments
to an Executor. An instantiating class implements an operation
that the Executor is required to perform on the target host.
"""

from abc import abstractmethod


class Task:

    @abstractmethod
    def run(self):
        """
        An operation that the Task object performs
        on the target host. The method should always
        return a string containing the results of the
        operation. If there are no results, an empty string
        should be returned.
        """

        pass
