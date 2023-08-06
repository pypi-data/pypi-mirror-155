# pylint: disable=too-few-public-methods

# module-level docstring
__doc__='''
OS detection module
===================

Straightforward OS detection, for when platform-specific code must
be written.

I am not the original author of this class. It was downloaded from:
https://github.com/scivision/pybashutils/blob/master/pybashutils/os_detect.py

'''

from platform import system, uname

class Os:
    """
    returns class with properties:
    .cygwin   Cygwin detected
    .wsl      Windows Subsystem for Linux (WSL) detected
    .mac      Mac OS detected
    .linux    Linux detected
    .windows  Windows detected
    .bsd      BSD detected
    """

    def __init__(self):
        syst = system().lower()

        # initialize
        self.cygwin = False
        self.wsl = False
        self.mac = False
        self.linux = False
        self.windows = False
        self.bsd = False

        if 'cygwin' in syst:
            self.cygwin = True
            self.os = 'cygwin'
        elif 'darwin' in syst:
            self.mac = True
            self.os = 'mac'
        elif 'linux' in syst:
            if 'Microsoft' in uname().release:
                self.wsl = True
                self.os = 'wsl'
            else:
                self.linux = True
                self.os = 'linux'
        elif 'windows' in syst:
            self.windows = True
            self.os = 'windows'
        elif 'bsd' in syst:
            self.bsd = True
            self.os = 'bsd'

    def __str__(self):
        return self.os
