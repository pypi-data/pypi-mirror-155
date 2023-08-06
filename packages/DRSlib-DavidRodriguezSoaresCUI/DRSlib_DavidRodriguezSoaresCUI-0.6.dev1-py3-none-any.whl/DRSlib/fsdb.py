# pylint: disable=broad-except, eval-used

# module-level docstring
__doc__='''
FileSystemDataBase
==================

A collection of tools for having a cached representation of
a file system.
'''

from pathlib import Path
import re
import json
from typing import Callable, Union, List, Dict, Iterable
import logging
from .decorators import timer
from .path_tools import ensure_dir_exists, make_FS_safe, folder_get_file_count
from .str_utils import truncate_str
from .utils import pickle_this, unpickle_this
log = logging.getLogger( __file__ )


def FSindex( root: Path, condition: Callable = lambda x: True ) -> Dict[str,dict]:
    ''' Returns a dictionnary such as
    - Contains <root_path:str> as only key
    - Recursively represents contained files and subdirectories, with each their subdirectories, etc
    '''
    assert root.is_dir()
    _root = root.resolve()

    def recursive_collection( _dir: Path ):
        def try_recursion( location: Path ):
            try:
                return recursive_collection( location ) if location.is_dir() else None
            except Exception as e:
                print(f"FSindex: something went wrong at '{root}'. Error:\n{e}")
                return None

        return {
            str(child.name): try_recursion( child )
            for child in _dir.iterdir()
            if condition( child )
        }

    root_s = root.as_posix()
    if root_s[-1] == '/':
        root_s = root_s[:-1]

    return {
        root_s: recursive_collection( root )
    }


class CachedFS:
    ''' Caching a filesystem tree can be useful for applications
    with frequent file system lookups.
    
    Features :
     - Possiblity to backup to/load from JSON file
     - cache directories, files, or both
    '''

    def __init__( self, root: Path, directories: bool = True, files: bool = True, backup_fs: dict = None ) -> None:

        if backup_fs:
            self.root = Path( backup_fs['root'] )
            assert root.samefile(self.root), f"ERROR: given root path '{root}' is different from backup root path '{self.root}' !"
            assert self.root.is_dir(), f"It seems root='{self.root}' is no longer a valid directory !"
            self.filter_text = backup_fs['filter']
            self.filter = eval( backup_fs['filter'] )
            self.fs = backup_fs['fs']

        else:
            assert files or directories, "CachedFS cannot be instantiated with directories=files=False."
            assert root.is_dir(), f"root='{root}' is not a valid directory"
            self.root = root.resolve()
            condition = ' or '.join( [
                x
                for x in [
                    'x.is_dir()' if directories else None,
                    'x.is_file()' if files else None
                ]
                if x is not None 
            ] )
            self.filter_text = f'lambda x: {condition}'
            self.filter = eval( self.filter_text )
            self.update()
        
        
    @timer
    def update( self ) -> None:
        ''' Updates internal DB '''
        self.fs = FSindex( self.root, self.filter )


    def __contains__( self, pattern: str ) -> bool:
        ''' Implements `<pattern:str> in <_:CachedFS>` operation
        '''
        _pattern = re.compile(pattern, flags=re.IGNORECASE )

        return 0 < len( self.search( 
            search_for=_pattern,
            stop_at_first=True
        ) )


    @timer
    def search( self, search_for: Union[str,re.Pattern,Callable], stop_at_first: bool = False ) -> List[str]:
        ''' Performs a search on internal FileSystem representation.

        `search_for`: Match criterion. Can be a string (matches file/directory name; case insensitive),
        a re.Pattern (matches with re.Pattern.match()) or a callable (must return boolean values; match
        on True).

        `stop_at_first`: returns at most one matching item.
        '''

        if callable(search_for):
            _search_for = search_for
        if isinstance(search_for, re.Pattern):
            _search_for = lambda x: bool(search_for.match(x))
        if isinstance(search_for, str):
            search_for_lower = search_for.lower()
            _search_for = lambda x: search_for_lower in x.lower()

        combine_paths = lambda x,y: f"{x}/{y}" if x else y

        def search_recursive( FSDB: dict, path_prefix: str = '' ):
            matches = list()
            #print(f"search_recursive: from '{path_prefix}'")
            try:
                for item, children in FSDB.items():
                    if _search_for( item ):
                        #print(f"Positive: '{item}'")
                        matches.append( combine_paths( path_prefix, item ) )
                        if stop_at_first:
                            return matches
                    if children:
                        matches.extend( 
                            search_recursive( children, combine_paths( path_prefix, item ) )
                        )
                    if stop_at_first and matches:
                        return matches
            except Exception as e:
                print(f"search_recursive: something went wrong at '{path_prefix}'. Error:\n{e}")
                raise
            
            return matches
        
        return search_recursive( self.fs )


    def as_json( self ) -> str:
        ''' Dumps CachedFS as json-formatted string '''
        data = {
            'root': str(self.root),
            'fs': self.fs,
            'filter': self.filter_text
        }
        return json.dumps( data, indent=2 )

    
    def backup_to_file( self, backup_file: Path ) -> None:
        ''' Dumps CachedFS to json-formatted file '''
        assert backup_file.suffix.lower() == '.json'
        backup_file.write_text( self.as_json(), encoding='utf8' )


    @classmethod
    def from_file( cls, backup_file: Path, root: Path ):
        ''' Loads CachedFS from json-formatted string produced by CachedFS.backup_to_file() function.
        Note: `root` is required to verify the intended root matches root in cache file.
        '''
        assert backup_file.suffix.lower() == '.json'
        backup = json.loads( backup_file.read_text( encoding='utf8' ) )
        return CachedFS( root=root, backup_fs=backup )
    

def get_snapshot_file( snapshot_folder: Path, snapshot_filename: str ) -> Path:
    ''' Returns a snapshot file path, given snapshot folder path and a filename 
    (which passes through a sanitization process).
    '''
    
    ensure_dir_exists( snapshot_folder )
    FS_safe_snapshot_filename = make_FS_safe( snapshot_filename + '.snapshot' )
    snapshot_file = snapshot_folder / FS_safe_snapshot_filename

    # Multiple reasons may lead to OSErrors for a given path
    try:
        snapshot_file.is_file()
    except OSError as e:
        try: # Correction: trucnating file name to 240 characters
            snapshot_file = snapshot_folder / truncate_str( 
                FS_safe_snapshot_filename, 
                output_length=240
            )
            snapshot_file.is_file()
        except OSError:
            raise OSError("get_snapshot_file: Snapshot file inaccessible for unforeseen reasons (FIXME!).") from e

    return snapshot_file


def get_folder_snapshot_h( _root: Path, extentions: Iterable[str], snapshot_folder: Path, recursive: bool = True, simplified: bool = False, rec: bool = False ) -> dict:
    ''' Recursive helper function to `get_folder_snapshot`.
    For more information see its docstring.
    '''

    # '*.txt' -> 'txt' extension conversion
    extentions = [ e.replace('*.','.') for e in extentions ]

    # Check for cached results
    cache_file_name = str(_root) + ('.S' if simplified else '.C')
    cache_file = get_snapshot_file( snapshot_folder, cache_file_name )
    try:
        res = unpickle_this( cache_file )
    except Exception:
        res = None
    if res:
        if simplified:
            log.info( "get_folder_snapshot: loaded from cache" )
            return res
        # Check for discrepancy in file number, as indicator something changed and snapshot should be rebuilt
        nbfiles1, nbfiles2 = res['__nbfiles__'], folder_get_file_count( _root )
        if nbfiles1==nbfiles2:
            log.info( "get_folder_snapshot: loaded from cache" )
            return res
        log.debug("get_folder_snapshot: number of files changes (%s != %s) -> updating snapshot", nbfiles1, nbfiles2)

    # Build from scratch
    log.info("get_folder_snapshot: from '%s' ..", _root)
    content = dict()

    if simplified: # "simplified" version
        for item in _root.iterdir():
            if item.is_file():
                (name, ext) = (item.stem, item.suffix)
                if ext not in extentions:
                    continue
                content[name] = item.resolve()
            elif item.is_dir():
                if not recursive:
                    continue
                content_rec = get_folder_snapshot_h( item, extentions, snapshot_folder, recursive, simplified, rec=True )
                content.update( content_rec )
            else:
                raise ValueError("get_folder_snapshot::Not file or folder : {}".format(item))
                
    else: # "complex" version
        file_count = 0
        for item in _root.iterdir():
            if item.is_file():
                (name, ext) = (item.stem, item.suffix)
                if ext not in extentions:
                    continue
                content[name] = item.resolve()
                file_count += 1
            elif item.is_dir():
                if not recursive:
                    continue
                content_rec = get_folder_snapshot_h( item, extentions, snapshot_folder, recursive, simplified, rec=True )
                content[item.name] = content_rec
                file_count += content_rec['__nbfiles__']
            else:
                raise ValueError("get_folder_snapshot::Not file or folder : {}".format(item))

        # Add file count
        content['__nbfiles__'] = file_count
        log.debug("get_folder_snapshot: from '%s' : found %s files !", _root, file_count)

    # Caching for later use
    if not (simplified and rec):
        pickle_this( content, cache_file )

    return content


def get_folder_snapshot( _root: Path, extentions: Iterable[str], snapshot_folder: Path, recursive: bool = True, simplified: bool = False ) -> dict:
    ''' Recursively builds a dictionnary representation of a directory tree. Only listed file extensions are considered.

    `extensions` : iterable of ``'*.ext'`` or ``'.ext'``

    Rules ("complex") :
     - The returned dictionnary has one entry : 'root'
     - An entry E can have one of three values according to  :
       > E is a directory : its value is a dictionnary with name of contained items as keys
       > E is a file : its value is its path (string format)
     - Each directory has one special entry '__nbfiles__', the recursive file count

    ex : let the following tree::

        <root>
            --A
                --T
                    -->file8.png
                -->file7.txt
                -->file4.jpg
            --C
                -->file5.git
            --G
            -->file3.log

    will have representation ::

        {
            '<root>': {
                'A': {
                    'T': {
                        'file8': '<root>/A/T/file8.png',
                        '__nbfiles__': 1
                    },
                    'file7': '<root>/A/file7.txt',
                    'file4': '<root>/A/file4.jpg',
                    '__nbfiles__': 3
                },
                'C': {
                    'file5': '<root>/A/file5.git',
                    '__nbfiles__': 1
                },
                'G': None,
                'file3' : '<root>/file3.log',
                '__nbfiles__': 5
            }
        }

    Rules ("simplified"):
     - Returns a dictionnary without nesting
     - All entries are files (with matching extension) with format : <filename:str> : <absolute file path:Path>

    Representation for previous tree::

        {
            'file3': '<root>/file3.log',
            'file4': '<root>/A/file4.jpg',
            'file5': '<root>/A/file5.git',
            'file7': '<root>/A/file7.txt',
            'file8': '<root>/A/T/file8.png'
        }
    '''
    ensure_dir_exists( snapshot_folder )
    return get_folder_snapshot_h( _root, extentions, snapshot_folder, recursive, simplified )
