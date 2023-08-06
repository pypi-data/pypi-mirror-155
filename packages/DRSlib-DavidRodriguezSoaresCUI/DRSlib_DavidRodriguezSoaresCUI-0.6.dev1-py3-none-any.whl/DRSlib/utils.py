
# module-level docstring
__doc__='''
General Utils module
====================

A collection of tools that do not fit in other modules.
'''

import pickle
from pathlib import Path
from typing import Any, Union, Iterable
import collections
import logging
log = logging.getLogger( __file__ )

# Used to be: "[%(levelname)s:%(filename)s:%(lineno)d] %(message)s"
LOG_FORMAT = "[%(levelname)s:%(funcName)s] %(message)s"

def pickle_this( data: Any, save_file: Path ) -> None:
    ''' Stores `data` to a file
    '''
    with save_file.open(mode="wb") as fp:   #Pickling
        pickle.dump(data, fp)
        log.debug( "Successfully stored data to file %s.", save_file )
        

def unpickle_this( save_file: Path ) -> Any:
    ''' Reads data from a file that was created by `pickle_this`
    '''
    if not save_file.is_file():
        log.debug( "Could not find file %s.", save_file )
        return None
    with save_file.open(mode="rb") as fp:   # Unpickling
        log.debug( "Successfully retrieved data from file %s.", save_file )
        return pickle.load(fp)


def is_iterable( a: Any ) -> bool:
    ''' Checks if object is iterable, thus having attribute `__iter__`.

    Bugfix 2021-11-09: hasattr(a, "__iter__") was true on type str

    Potential future fix: According to collections.abc.Iterable, "The only reliable way to determine whether an object is iterable is to call iter(obj)."
    See method 3 at https://www.geeksforgeeks.org/how-to-check-if-an-object-is-iterable-in-python/
    '''
    return isinstance( a, collections.abc.Iterable ) 


def type_assert( v: object, v_name: str, expected_type: Union[type, Iterable[type]], prefix: str, accept_none: bool = False ) -> None:
    ''' Makes sure a variable is of given type(s).

    Raises AssertionError if `v` has type not covered by `expected_type`.

    `prefix` : A string prefix for the message the raised error may display, useful for knowing which
               part of the code generated the error. eg: 'MyClass.method2'

    `accept_none` : if True, accepts a `None` value for `v` no matter the expected type(s). 
                    Alternatively, include `type(None)` to the expected type list.
    '''
    # Case 1 : accept None value
    if accept_none is True and v is None:
        return

    error_txt = f"{prefix}: expected received '{v_name}' to be a {expected_type} object, received '{type(v)}'"
    # Case 2 : expected_type is a list/set => recursion
    if is_iterable(expected_type):
        for e_t in expected_type:
            try:
                type_assert( v, v_name, e_t, prefix, accept_none )
                return
            except AssertionError:
                continue
        raise AssertionError( error_txt )
    
    # Default case : check type
    assert isinstance( v, expected_type ), error_txt
