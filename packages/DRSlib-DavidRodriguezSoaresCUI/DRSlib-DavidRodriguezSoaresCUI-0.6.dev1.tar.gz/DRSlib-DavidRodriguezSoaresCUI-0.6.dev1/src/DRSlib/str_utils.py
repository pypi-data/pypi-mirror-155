# pylint: disable=too-many-return-statements

# module-level docstring
__doc__='''
String-focused utils
====================

Simple utils that accomplish one task well, specifically string operations.

'''
 
import re

def ensure_double_quotes( s: str ) -> str:
    ''' Ensures s is double quoted in a particular way :
     - returned string must begin and end with a double quote character `"`
     - any double quote that isn't at the beginning or end must be escaped `\\"`

    Examples :
     - `` (empty string) -> `""`
     - `.` -> `"."`
     - `hello` -> `"hello"`
     - `"hello` -> `"hello"`
     - `hello"` -> `"hello"`
     - `"hello"` -> `"hello"` (unchanged)
     - `"he"llo` -> `"he\\"llo"`
     - `"he\\"llo"` -> `"he\\"llo"` (unchanged)

    '''

    if not s:
        return '""'
    if len(s)==1:
        if s[0]=='"':
            return '"\\""'
        return '"' + s + '"'
    # else
    if s[0] != '"':
        return ensure_double_quotes( '"' + s )
    if s[-1] != '"':
        return ensure_double_quotes( s + '"' )

    # past this point, 2 <= len(s) and there are double quotes at the beginning and end of s.
    
    double_quote_locations = set( m.start() for m in re.finditer(r'"', s) )
    escaped_double_quote_locations = set( m.start()+1 for m in re.finditer(r'\\"', s) )
    double_quote_locations.difference_update( escaped_double_quote_locations )

    # s lacks any double quotes
    if not double_quote_locations:
        return '"' + s + '"'

    # detection of double quotes to escape
    proper_double_quote_location = set( [0, len(s)-1] )
    misplaced_double_quotes = set(double_quote_locations).difference( proper_double_quote_location )
    # print(f"proper_double_quote_location={proper_double_quote_location}")
    # print(f"double_quote_locations={double_quote_locations}")
    # print(f"misplaced_double_quotes={misplaced_double_quotes}")
    
    # s is already properly double quoted
    if not misplaced_double_quotes:
        return s

    # escaping double quotes plus recursion
    s_characters = list(s)
    misplaced_DQ_idx = misplaced_double_quotes.pop()
    _s = ''.join( s_characters[:misplaced_DQ_idx] + [ '\\', '"' ] + s_characters[misplaced_DQ_idx+1:] )
    return ensure_double_quotes( _s )


def truncate_str( s: str, output_length: int, cut_location: str = 'center' ) -> str:
    ''' Truncates string to a new length
    
    `cut_location` : (default:'center') in ['left','center','right']
    ''' 
    s_len = len(s)
    if s_len <= output_length:
        return s 
    if output_length <= 7:
        print(f"Warning: used truncate_str with 'output_length'={output_length}<=7, which is too low and would probably result in undesired results, so 's' was returned unchanged !")
        return s

    #len_diff = s_len-output_length
    if cut_location=='left':
        return f"{ s[:output_length-6] } [...]"
    if cut_location=='center':
        offset = (output_length // 2) - 3
        return f"{ s[:offset] } [...] { s[-(offset - (1 if output_length%2==0 else 0)):] }"

    if cut_location=='right':
        return f"[...] { s[-(output_length-6):] }"
    # else
    raise ValueError(f"truncate_str: given parameter 'cut_location'={cut_location} is not in ['left','center','right'] !")


if __name__=='__main__':

    # ensure_double_quotes tests

    # tests = [
    #     '',
    #     '.',
    #     '"',
    #     '"hello',
    #     'hello"',
    #     '"hello"',
    #     '"he"llo"',
    #     'he\\"llo'
    # ]

    # for test_s in tests:
    #     res = ensure_double_quotes(test_s)
    #     print(f"test_s={test_s}={list(test_s)} -> {list(res)} = {res}")


    # truncate_str tests

    tests = [
        'h'* 20,
        'h' * 21
    ]
    for new_len in [10,15]:
        for cut in ['left','center','right']:
            for test_s in tests:
                res = truncate_str( test_s, new_len, cut)
                print(f"new_len={new_len}, cut={cut} : test_s='{test_s}' (len={len(test_s)}) -> '{res}' (len={len(res)})")
