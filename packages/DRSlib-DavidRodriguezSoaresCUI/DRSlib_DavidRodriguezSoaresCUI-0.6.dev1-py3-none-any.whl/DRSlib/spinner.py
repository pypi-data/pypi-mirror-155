# pylint: disable=broad-except

# module-level docstring
__doc__='''
CLI text-based spinning animation
=================================

An exceedingly simplistic progress animation library.
'''

import itertools
import os
import sys
from .str_utils import truncate_str

class MySpinner:
    ''' My simple spinner, one-function, easy to use and supports text
    on the left of the spinning wheel !
    
    Usage example::

        spinner = MySpinner()
        nb_items = len(items_to_process)
        for idx, item in enumerate(items_to_process):
            if idx%10==0:
                spinner.animation( text=f"Progress: {100*idx/nb_items:.1f}%" ) 
            process_item( item )
            
    '''

    def __init__( self ) -> None:
        self.last_txt_len = 0
        self.spinner = itertools.cycle(['-', '\\', '|', '/'])
        try:
            self.terminal_width = os.get_terminal_size().columns
        except Exception as e:
            print(f"MySpinner: Could not get terminal width, defaulting to 40 columns. Got error {e}")
            self.terminal_width = 40
        # print(f"MySpinner: terminal width is {self.terminal_width}")


    def animation( self, text: str = '', no_spinner: bool = False ):
        ''' update animation, with the option to print text on the left of the
        spinner character
        '''
        tmplen = (self.last_txt_len + 1)
        # erase previous message
        # why do backspaces, then whitespace, then backspaces again :
        # because backspace alone didn't consistently erase previous text
        sys.stdout.write( '\b' * tmplen + ' ' * tmplen + '\b' * tmplen ) 

        # write new message, truncated to not overflow terminal width (necessary for best results)
        spinner_symbol = '' if no_spinner else next(self.spinner)
        message = truncate_str(
            text + spinner_symbol,
            output_length=self.terminal_width-1, 
            cut_location='center'
        )
        sys.stdout.write( 
            message
        ) 
        sys.stdout.flush()
        self.last_txt_len = len( message ) - (0 if no_spinner else 1)

    def clear( self ):
        ''' erase spinner character (and accompanying text)
        '''
        self.animation( no_spinner=True )
