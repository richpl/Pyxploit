#! /usr/bin/python

"""
Task object which obtains a Windows process list
by running the 'tasklist' command.

Since the output is unpredictable, the following
doctest will return an error, but illustrates
use of the Task object.

>>> tasklist = Tasklist()
>>> tlist = tasklist.run()
>>> print(tlist)
"""

import os
from task import Task


class Tasklist(Task):

    def run(self):

        # Execute 'tasklist' and obtain
        # a file handle connected to the
        # output pipe
        cmd = "tasklist"
        output = os.popen(cmd, mode='r', buffering=1)

        # Read from the file and accumulate the
        # results into a string
        tlist = ""
        for line in output.readlines():
            tlist = tlist + line

        return tlist

    if __name__ == "__main__":
        import doctest
        doctest.testmod()
