####
loggerutils
####
loggerutils 0.0.1

*****
About
*****
This module contains a simple set of tools designed to make logging to
the python built-in logger module easier for some scenarios. Currently it
only contains one class called LogStream. I will probably be expanding
it in the future.

************
Installation
************
::

    $ git clone git://github.com/nickryand/loggerutils.git
    $ cd loggerutils
    $ python setup.py install

*****
Usage
*****
::

    import logging
    import subprocess

    from loggertools.logstream import LogStream

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()

    proc = subprocess.Popen(["seq", "-w", "1", "10000"],
                            stdout=subprocess.PIPE)

    info_logstream = LogStream(logger, proc.stdout)
    info_logstream.start()

    proc.wait()
    info_logstream.join()


Copyright (c) 2013 Nick Downs <nickryand@gmail.com>
