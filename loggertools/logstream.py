#!/usr/bin/env python
#
# The MIT License
#
# Copyright (c) 2013 Nicholas Downs
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

"""
A module that provides a very simple implementation of a text file stream
reader that sends messages to a logger.
"""

import os
import io
import logging
import subprocess
import threading

class LogStreamError(Exception): pass

class LogStream(threading.Thread):
    """Simple class that reads lines from a file descriptor and logs them"""

    def __init__(self, logger, descriptor, level=logging.INFO, close_fd=True):
        super(LogStream, self).__init__()

        self.logger = logger
        self.level = level
        self.descriptor = descriptor
        self.close_fd = close_fd

        self._handle = None

    def run(self):
        # XXX: This should maybe support additional types of reading instead
        #      of just readline()
        if isinstance(self.descriptor, int):
            self._handle = io.open(self.descriptor, "r")
        elif hasattr(self.descriptor, 'readline'):
            self._handle = self.descriptor
        else:
            raise LogStreamError("Stream needs to be a valid file descriptor"
                                 " or an open file-like handle which supports"
                                 " the readline() method")

        while True:
            line = self._handle.readline()
            if not line:
                break
            self.logger.log(self.level, line.strip())

        if self.close_fd:
            self._handle.close()

def example():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("subprocess")

    proc = subprocess.Popen(["seq", "-w", "1", "10000"],
                            stdout=subprocess.PIPE)

    info_logstream = LogStream(logger, proc.stdout)
    info_logstream.start()

    proc.wait()
    info_logstream.join()

if __name__ == "__main__":
    example()
