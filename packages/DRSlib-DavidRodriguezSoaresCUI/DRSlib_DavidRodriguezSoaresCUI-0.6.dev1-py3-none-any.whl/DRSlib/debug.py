# module-level docstring
__doc__='''
Debugging utils
===============

Deubgging is made easier with these convenience functions.
'''

from typing import Callable, Any, Union
import functools
import re
import shutil
import traceback

FUNC_RELEVANT_ATTR={
    '__annotations__',
    '__class__',
    '__defaults__',
    '__dict__',
    '__doc__',
    '__kwdefaults__',
    '__module__',
    '__name__',
    '__qualname__'
}

def func_attribute_printout( user_funtion: Callable ) -> None:
    ''' Prints relevant attributes of `user_function`, with attribute name, value and type.
    Relevant attributes are in `FUNC_RELEVANT_ATTR`.

    Usage example: reviewing an unfamiliar imported function::
    
        from some.module import foo
        func_attribute_printout( foo )
    
    Output::

        foo.__annotations__ = ...
        [...]
        foo.__qualname__ = foo, type=str
        
    '''
    f_name = user_funtion.__name__
    for attr in dir(user_funtion):
        if attr in FUNC_RELEVANT_ATTR:
            attr_val = user_funtion.__getattribute__(attr)
            print(f"{f_name}.{attr} = {attr_val}, type={type(attr_val)}")


regex_var_name_from_call = re.compile(r'\(\s*(?:var\s*=\s*)?([^,\ ]+).*\).*$')

def debug_var( var: Any, var_name: str = None ) -> None:
    ''' Prints the name, value and type of a variable, typically used during development
    for quick and easy type/value sanity checks.

    Warning: if debug_var is decorated, automatic variable name retrieval doesn't work !
             You will need to specify var_name.

    Automatic variable name retrieval : in most situations `debug_var` should be able to 
    retrieve the name of the variable using the `traceback` module. If it fails, simply
    add it manually. This feature was inspired by code snippets from 
    https://stackoverflow.com/questions/2749796/how-to-get-the-original-variable-name-of-variable-passed-to-a-function

    Usage example : you want to add a sanity check to a received value::
    
        ...
        res = do_something()
        debug_var( res )
        ...

    Output::
    
        >>> DEBUG VAR: res=[1999, 2011] (list)

    Note : during development a different method for retrieving var_name automatically
    was found. It used the stack module. Unfortunately it was found to be
    significantly slower and to not have any significant advantage so it was removed.
    You can find the implementation here below::
    
        # inspect method : similar but extract locals from frame(s) and try to find
        stack = inspect.stack()[2:]
        for frameinfos in stack:
            lcls = frameinfos.frame.f_locals
            for name in lcls:
                if id(var) == id(lcls[name]):
                    var_name = name
                    break
            if var_name:
                break
    

    Performance : tested on a AMD 1700 using the standard Python 3.9 interpreter,
    which used only 1 execution thread. Executed 10 iteration in ~2ms and 100'000
    iterations in ~11.8s (~9 iter/ms). Figures for indicative purposes only.
    '''

    # If `var_name` isn't specified, we try to retrieve this information
    if var_name is None:
        # traceback method : extract stack frame to retrieve call code ..
        raw_call_traceback = traceback.extract_stack( limit=2 )[0]
        call_code_line = raw_call_traceback.line
        # .. then extract variable name from call to `debug_var` using regular expression (handles both args and kwargs)
        var_name = regex_var_name_from_call.search(call_code_line).groups()[0]

    if not var_name:
        var_name = "error:Couldn't determine variable name automatically. Pleasy try to pass variable name as argument."
    print( f"DEBUG VAR: {var_name}={var} ({type(var)})")


def call_progress( expected_argument: Union[Callable,str] ) -> Callable:
    ''' Decorator. Typically used to make the execution status of 
    a function verbose when developping.
    The decorated function's execution is enclosed in a text-based
    box, with pre/post-execution message. 

    `expected_argument`: Optional string argument, replaces the default
    message (user_function.__name__).

    Usage example: decorating debug_var (see warning in debug_var's docstring)::
    
        decorated_debug_var = call_progress("debug_var debugs a variable")(debug_var)
        hello='world'
        decorated_debug_var( var=hello, var_name='hello' )

    Output::

        ----------------------------------------
        debug_var debugs a variable ..
        DEBUG VAR: hello=world (<class 'str'>)
        debug_var debugs a variable done
        ----------------------------------------
    
    
    Note: this example is not great: decorating manually (not with @call_progress syntax)
    and decorating a function that specifically advises against decoration. But this showcases
    an actual use case that works.
    '''

    def actual_decorator( user_function: Callable ) -> Callable:

        @functools.wraps( user_function )
        def wrapper( *args, **kwargs ) -> Any:
            nonlocal user_function

            box_W = min( shutil.get_terminal_size().columns, 40 )
            
            print( '-' * box_W )
            print( printout_text + ' ..' )
            res = user_function( *args, **kwargs )
            print( printout_text + ' done' )
            print( '-' * box_W )

            return res

        return wrapper

    if callable( expected_argument ):
        # decorator_with_arguments was run without argument => use 
        # default values for expected arguments or raise error
        user_function = expected_argument
        printout_text = user_function.__name__
        return actual_decorator(user_function)

    if isinstance(expected_argument, str):
        printout_text = expected_argument
        return actual_decorator

    raise ValueError(f"call_progress: `expected_argument` of type {type(expected_argument)} is not in Union[Callable,str] !")
