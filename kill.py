#! /usr/bin/python

"""
Task object which can be used to signal the Agent
running on the target box that it should terminate.

>>> kill = Kill()
>>> result = kill.run()
>>> print(result)
killed
"""

import os
from task import Task


class Kill(Task):

    def run(self):
        """
        The only output returned is a string to indicate that
        the task executed, specifically "killed".
        """

        return "killed"

    if __name__ == "__main__":
        import doctest
        doctest.testmod()
