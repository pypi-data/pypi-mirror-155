# module-level docstring
__doc__='''
General-purpose decorators
==========================

This file contains useful (function) decorators !

Also, you can find :
 - a structure convention for all function decorators
 - tests for each decorator (see at the bottom of the file; run the file to execute them)

'''

from typing import Any, Callable, Union
import time
import datetime
import logging
from pathlib import Path
import pickle

# functool.wraps is a decorator for wrappers that copies informations from 
# the original function to the wrapper, allowing for transparently chaining decorators
import functools
# for profiling
import cProfile
import pstats 


########### CONVENTION ###########
# Any decorator in this file must 
# follow this format; please use it
# as a template :
########### CONVENTION ###########

def decorator_without_argument( user_function: Callable ) -> Callable:
    '''
    DOCSTRING
    '''

    # maybe do something here

    @functools.wraps( user_function )
    def wrapper( *args, **kwargs ) -> Any:
        nonlocal user_function

        # maybe do something before calling f
        res = user_function( *args, **kwargs )
        # maybe do something after calling f
        return res

    return wrapper
    

def decorator_with_arguments( expected_argument: Any ) -> Callable:
    '''
    DOCSTRING
    '''

    def actual_decorator( user_function: Callable ) -> Callable:

        # maybe do something here

        @functools.wraps( user_function )
        def wrapper( *args, **kwargs ) -> Any:
            nonlocal user_function
            
            # maybe do something before calling f
            res = user_function( *args, **kwargs )
            # maybe do something after calling f

            return res

        return wrapper

    if callable( expected_argument ):
        # decorator_with_arguments was run without argument => use 
        # default values for expected arguments or raise error
        user_function = expected_argument
        return actual_decorator(user_function)

    # decorator_with_arguments was run with argument (maybe do something here)

    return actual_decorator


########### progress tracking ###########

def call_progress( message: str ) -> Callable:
    ''' Prints progress of a callable to stdout
    '''

    def actual_decorator( user_function: Callable ) -> Callable:

        # maybe do something here

        @functools.wraps( user_function )
        def wrapper( *args, **kwargs ) -> Any:
            nonlocal user_function, message
            
            print("-"*40)
            print( message + ' ..' )
            res = user_function( *args, **kwargs )
            print( message + ' OK!' )
            print("-"*40)

            return res

        return wrapper

    assert isinstance( message, str ), "message must be a string"

    return actual_decorator


########### timing ###########

def timer( user_function: Callable ) -> Callable:
    '''
    Prints how much time user function took to run
    '''

    @functools.wraps( user_function )
    def wrapper( *args, **kwargs ) -> Any:
        nonlocal user_function

        t_start = time.time()
        res = user_function( *args, **kwargs )
        elapsed_ms = int( 1000 * (time.time() - t_start) )
        print(f"Function {user_function.__name__} ran for {elapsed_ms}ms.")
        return res

    return wrapper


def profile( user_function: Callable ) -> Callable:
    ''' Profiling is an advanced technique to measure
    code execution time. 

    This decorator was heavily inspired from mCoding's video:
    https://www.youtube.com/watch?v=m_a0fN48Alw

    Using PROF output file : you need the `snakeviz` package
    installed (`pip install snakeviz`). Simply type
    `snakeviz <profile file>`
    in a terminal and you should see a web browser window with 
    visualizations of the profile.
    '''

    @functools.wraps( user_function )
    def wrapper( *args, **kwargs ) -> Any:
        nonlocal user_function

        # Create profiler and run user function
        with cProfile.Profile() as _profile:
            res = user_function( *args, **kwargs )
        
            # Store results
            stats = pstats.Stats( _profile )
            stats.sort_stats( pstats.SortKey.TIME )
            stats.dump_stats(filename=f'profile_{user_function.__name__}.prof')

        return res

    return wrapper


def minimum_duration( min_duration_s: Union[float,int] ) -> Callable:
    ''' Makes sure the callable's execution takes no less than
    ``min_duration_s`` seconds to execute, using the ``time``
    library's functions.

    Usage example: Avoid getting banned for spamming requests::

        ban_safe_urlopen = minimum_duration( min_duration_s=0.5 )( urllib.request.urlopen )
        for url in URLs:
            with ban_safe_urlopen(url) as f:
                ...
        
    '''

    def actual_decorator( user_function: Callable ) -> Callable:

        @functools.wraps( user_function )
        def wrapper( *args, **kwargs ) -> Any:
            nonlocal user_function, min_duration_s
            
            start_time = time.time()
            res = user_function( *args, **kwargs )
            time_to_skip = min_duration_s - (time.time() - start_time)
            if time_to_skip > 0:
                time.sleep( time_to_skip )

            return res

        return wrapper

    assert isinstance( min_duration_s, (float,int) ), "minimum_duration: Omitted parameter `min_duration_s`."

    return actual_decorator


########### logging ###########


def log_to_file( user_function: Callable ) -> Callable:
    '''
    Logs function call to file
    '''
    
    logging.basicConfig( 
        filename=f"{user_function.__name__}.log",
        level=logging.INFO
    )
    _log = logging.getLogger( user_function.__name__ )

    @functools.wraps( user_function )
    def wrapper( *args, **kwargs ) -> Any:
        nonlocal user_function

        str_args = ', '.join([
            str(arg) 
            for arg in args
        ])
        _now = datetime.datetime.now()
        res = user_function( *args, **kwargs )

        _log.info(
            "Called function %s with args=[%s] and kwargs=%s at %s, with return value %s.", 
            user_function.__name__,
            str_args,
            kwargs,
            _now,
            res
        )
        
        return res

    return wrapper


########### caching ###########


def cacheFS( cache_file: Path ) -> Callable:
    '''
    Returns a decorator that caches the returned value of user function using a cache file.
    '''

    def actual_decorator( user_function: Callable ) -> Callable:
        ''' Caches the returned value of user function using a cache file. '''

        @functools.wraps( user_function )
        def wrapper( *args, **kwargs ) -> Any:
            nonlocal user_function, cache_file, cached_data
            
            k = (args, frozenset(kwargs.items()))
            if k in cached_data:
                # cache hit
                print(f"Cache hit for {user_function.__name__} with args={args} and kwargs={kwargs}.")
                return cached_data[k]
            
            # else: cache miss
            res = user_function( *args, **kwargs )
            cached_data[k] = res
            with cache_file.open( mode='wb' ) as f:
                pickle.dump( cached_data, f ) # update cache
            
            print(f"Written cache to file '{cache_file}'.")

            return res

        return wrapper


    def load_cached_data( cache_file: Path ) -> dict:
        if cache_file.is_file():
            try:
                with cache_file.open( mode='rb' ) as f:
                    cached_data = pickle.load( f )
            except EOFError:
                pass # cache file exists but doesn't contain anything/valid data
            else:
                return cached_data
        return dict()


    if callable( cache_file ):
        # cacheFS was run without argument => default filename
        user_function = cache_file
        cache_file = Path( f"{user_function.__name__}.cacheFS" )
        cached_data = load_cached_data( cache_file )
        return actual_decorator(user_function)

    # else: cacheFS was run with argument
    # File Extension enforcement
    if cache_file.suffix != '.cacheFS':
        cache_file = Path( f'{cache_file}.cacheFS' )

    cached_data = load_cached_data( cache_file )

    return actual_decorator


########### end of decorators ###########


if __name__=="__main__":

    def vspace():
        ''' just prints newlines '''
        print( '\n' * 2 )

    # Tests

    # Test 01
    vspace()
    print("Test 01 : decorator 'timer'")

    @timer
    def wait2s() -> None:
        ''' Just wait 2s '''
        time.sleep(2)

    print(wait2s)
    print(wait2s.__doc__)
    wait2s()

    # Test 02
    vspace()
    print("Test 02 : decorator 'log_to_file'")

    @log_to_file
    def add( a: int, b: int ) -> int:
        ''' Add a and b '''
        return a + b

    print(add)
    print(add.__doc__)
    add( 7, 13 )
    logfile = Path('add.log')
    assert logfile.is_file()

    # Test 03
    vspace()
    print("Test 03 : decorator 'cacheFS'")

    # @cacheFS( Path('slow_mult') )
    @cacheFS
    def slow_mult( a: int, b: int ) -> int:
        ''' Multiply a and b '''
        time.sleep(1)
        return a * b

    print(slow_mult)
    print(slow_mult.__doc__)

    @timer 
    def test03():
        ''' tests timer decorator '''
        for i in range(4):
            res = slow_mult( 111, 10*i )
            print(f"111 * {i} = {res}")

    test03() # runs in 2ms-4s depending on cache hits/misses
