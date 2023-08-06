# pylint: disable=eval-used, broad-except

# module-level docstring
__doc__='''
Command line user interface
===========================

Implements convenience function for CLI user interaction.
Useful when you need to ask the user what to do, or select one
of many options.
'''

from typing import Iterable, Union, Any, Callable, Dict, Optional
from pathlib import Path
import sys
import os

from .banner import one_line_banner
from .os_detect import Os
from .path_tools import folder_get_subdirs, windows_list_logical_drives, make_FS_safe

KBI_msg = "A KEYBOARDINTERRUPT WAS RAISED. THE PROGRAM WILL EXIT NOW."

def __input_KBI( message: str, exit_on_KBI: bool = True ) -> str:
    ''' Handles `KeyboardInterrupts` on `input` calls, used by other more complex functions.
    `exit_on_KBI`: If True, user can exit the program. If False, handling
    of KeyboardInterrupt is delegated to calling code.
    '''
    if exit_on_KBI:
        try:
            return input( message )
        except KeyboardInterrupt:
            print( KBI_msg )
            end_of_program()
    return input( message )


def pause() -> None:
    ''' Implements a 'pause' feature. Press ENTER to continue. If 'Ctrl+C' is pressed, 
    it exits the program '''

    __input_KBI( "Press the <ENTER> key to continue...", exit_on_KBI=False )


def end_of_program( exit_code: int = 0, halt: bool = False ) -> None:
    ''' Standardized way of ending programs '''
    print("\nEND OF PROGRAM\n")
    if halt:
        pause()
    sys.exit(exit_code)


def yes_or_no( message: str, retry: bool = True, default: bool = None, exit_on_KBI: bool = True ) -> bool:
    ''' User input fiels optimized for obtaining y/n answer.
    Loops user input until `KeyboardInterrupt` is raised (hard exit) or user types correct answer.
    `default` is returned if user input is inconclusive and `retry` is False.

    eg::

        >>> continue = yes_or_no( "Continue ?", retry=False, defalut=False )
        'Continue ? (y/n): '
        >>> confirm_date = yes_or_no( "Is the date correct ?" )
        'Is the date correct ? (y/n): '
        
    '''
    if not retry:
        assert default is not None and isinstance( default, bool )

    while True:
        default_txt = ' [default:y]' if default is True else ( ' [default:n]' if default is False else '' )
        raw_input = __input_KBI( 
            f"{message} (y/n){default_txt}: ",
            exit_on_KBI=exit_on_KBI
        ).lower()

        if raw_input=='' and default is not None:
            return default
        if raw_input[0] == 'y':
            return True
        if raw_input[0] == 'n':
            return False
        if retry:
            print("Invalid answer, try again")
            continue
        return default


def user_input( prompt: str, accepted: Union[Iterable[Union[str,int]],Callable], default: Any = None ) -> str:
    ''' Asks user for input, with restrictions on accpetable values.
    `prompt`: appropriate text asking the user for input. Should be straightforward and informative about the kind of data that is asked
    `accepted`: either a function testing if the user input is acceptable, or an iterable containing all acceptable values
    `default`: When given, if the user input is not acceptes, default is returned. When abscent, the user will be prompted again until either
    an accepted value is entered or a KeyboardInterrupt is raised.
    Note: this is only designed to retrieve values of the following types: str, int, float
    '''
    
    # Smart prompt reformat
    if default is not None:
        prompt += f"[default:{default}] "
    if prompt[-1] == ':':
        prompt += ' '
    elif prompt[-2:]!=': ':
        prompt += ': '

    acceptable_UI = lambda ui: accepted(ui) if callable(accepted) else (ui in accepted)
        
    while True:
        # main loop: ask user until an acceptable input is received, or a KeyboradInterrupt ends the program
        _user_input = __input_KBI( prompt )
        
        # case: raw user input is accepted
        if acceptable_UI( _user_input ):
            return _user_input
        
        # case: processed user input is accepted
        variations = [ 'int(_user_input)', 'float(_user_input)', '_user_input.lower()' ]
        for variation in variations:
            try:
                __user_input = eval( variation )
                if acceptable_UI( __user_input ):
                    return __user_input
            except (ValueError, AttributeError):
                pass
        
        # case: user input is not accepted AND there is a default
        if default is not None:
            return default
        
        # case: user input is not accepted AND there is no default => notify user, ask again
        print("Input '%s' is not a valid input. %s", _user_input, (f"Please choose one of : {accepted}" if not callable(accepted) else "") )


def choose_from_list( choices: list, default: int ) -> Any:
    ''' Prints then asks the user to choose an item from a list
    `default`
    '''
    # Print choices
    print( "Choices:\n  " + '\n  '.join([
        f"[{idx}] {choice}"
        for idx, choice in enumerate(choices)
    ]) + '\n' )

    # Get user selection
    idx = user_input( "Selection : ", accepted=list(range(len(choices))), default=default )

    # Return choice
    return choices[idx]


def select_action( choices: Dict[str,Callable], no_banner: bool = False, default: str = None, execute: bool = False ) -> Optional[Callable]:
    ''' Asks the user to choose an action amongst a list of labeled actions. Returns a callable
    corresponding to the chosen action if `execute` is False, executes it otherwise.
    
    Example of `choices`::

        choices = {
            'q': {
                'explanation': 'quit the program',
                'action': <function that exits the program:Callable>
            },
            ...
        }
    ''' 

    # Print banner
    if not no_banner:
        banner = one_line_banner( "Selection menu" )
        print(banner)

    accepted_inputs = choices.keys()

    # Print choices
    choice_formatter = lambda choice: choice + ( f" - {choices[choice]['explanation']}" if 'explanation' in choices[choice] else '' )
    print( "Choices:\n  " + '\n  '.join([
        choice_formatter( choice )
        for choice in accepted_inputs
    ]) + '\n' )
    
    # Get user choice
    _user_input = user_input( "Selection : ", accepted=accepted_inputs, default=default )

    # Return or execute corresponding callable
    if execute:
        choices[_user_input]['action']()
        return None
    
    return choices[_user_input]['action']


def cli_explorer( root_dir: Path = None, allow_mkdir: bool = True ) -> Path:
    ''' Allows for the user to explore directories to select one.
    '''

    sub_dirs = folder_get_subdirs( root_dir ) if root_dir else windows_list_logical_drives()
    cwd = root_dir
    
    def get_parent():
        try:
            return cwd.parent
        except Exception:
            return None

    while True:
        print(f"cwd : {cwd}")

        # Craft selection list
        selection_list = [ d.name if 0<len(d.name) else str(d) for d in sub_dirs ]
        extra_options = list()
        cwd_parent = get_parent()
        if cwd_parent:
            extra_options.append('..')
        if cwd:
            extra_options.append('.')
            if allow_mkdir:
                extra_options.append('<Make new folder here>')

        # ask user
        next_dir = choose_from_list( 
            choices=extra_options + selection_list,
            default=extra_options.index('.') if '.' in extra_options else None 
        )
        
        if next_dir=='..':
            if cwd==cwd_parent:
                # happens when at the root of a drive on windows
                sub_dirs = windows_list_logical_drives()
                cwd = None
                continue
            cwd = cwd_parent
        elif next_dir=='.':
            return cwd
        elif next_dir=='<Make new folder here>':
            while True:
                new_dir_name = user_input(
                    prompt="New folder name",
                    accepted=lambda x: isinstance(x, str)
                )
                new_dir = cwd / make_FS_safe(new_dir_name.replace('.',''))
                if new_dir.is_dir():
                    print(f"'{new_dir_name}' already exists !")
                    continue
                new_dir.mkdir()
                cwd = new_dir
                break
        else:
            cwd = sub_dirs[ selection_list.index( next_dir ) ]
        sub_dirs = folder_get_subdirs( cwd )


def clear_screen() -> None:
    ''' Clears the terminal screen, multi-platform '''
    _os = Os()
    if _os.windows or _os.cygwin:
        os.system( 'CLS' )
    elif _os.linux or _os.wsl:
        os.system( 'clear' )


def skipNlines( n: int ) -> None:
    ''' Skips n lines in the terminal; used for vertical whitespace '''
    assert n>0, "drslib::skipNlines: Invalid number of lines entered : '{}'".format(n)
    print('{}'.format('\n'*(n-1)))
