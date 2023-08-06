# pylint: disable=broad-except

# module-level docstring
__doc__='''
Shell command execution
=======================

Sometimes we just want to execute a shell command and possibly
retrieve stdout/stderr, without hassle.
'''

from typing import Iterable, Dict, Union
from subprocess import Popen, PIPE

def execute( command: Union[str,Iterable[str]], shell: bool = True ) -> Dict[str,str]:
    ''' Passes command to subprocess.Popen, retrieves stdout/stderr and performs
    error management.
    Returns a dictionnary containing stdX.
    Upon command failure, prints exception and returns empty dict. '''

    try:
        with Popen( command, stdout=PIPE, stderr=PIPE, shell=shell ) as process:
            # wait and retrieve stdout/err
            _stdout, _stderr = process.communicate()
            # handle text encoding issues and return stdX
            return {
                'stdout': _stdout.decode('utf8', errors='backslashreplace'),
                'stderr': _stderr.decode('utf8', errors='backslashreplace')
            }
    except Exception as e:
        print(f"execute: Error while executing command '{command}' : {e}")
        raise
