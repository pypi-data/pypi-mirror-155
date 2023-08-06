# module-level docstring
__doc__='''
MediaInfo interface
===================

An interface to software `MediaInfo <https://mediaarea.net/fr/MediaInfo>`_

Note: For it to work, MediaInfo needs to be installed on the system AND be
callable from a terminal.
'''

import logging
import re
from pathlib import Path
from typing import List, Dict, Union, Iterable

from .utils import type_assert
from .execute import execute

MEDIAINFO_POSSIBLE_RETURN_VALUES = Union[int,float,str,type(None)]

class Datapoint:
    ''' In this context, a Datapoint represents a multimedia parameter
    in a format compatible with MediaInfo's cli interface.
    
    Advantages:

    - systematic solution
    
    - integrates cli<->shorthand format conversion
    
    - ability to combine commands
    
    - shifts complexity from MediaInfo's class
    '''

    SEPARATOR = '\\n'

    def __init__( self, category: str, parameter: Union[str,List[str]] ):
        self.category = category
        self.parameter = parameter

    def __str__(self):
        parameter_s = Datapoint.SEPARATOR.join( self.parameter ) \
            if isinstance( self.parameter, list ) \
            else self.parameter
        return f"--Inform={self.category};" + parameter_s

    def __repr__(self):
        return f"< Datapoint : '{str(self)}' >"

    def __parameter_shorthand(self, p: str ):
        ''' Tries to convert parameter to its equivalent shorthand.
        Helper function for `parameter_shorthand`
        '''        
        for k,v in MediaInfo.DATAPOINTS.items():
            dp = Datapoint.from_string(v)
            if dp.parameter==p:
                return k
        return p 

    @property
    def parameter_shorthand(self):
        ''' Tries to convert parameter to its equivalent shorthand '''
        return self.__parameter_shorthand( self.parameter ) \
            if isinstance( self.parameter, str ) \
            else [
                self.__parameter_shorthand( p )
                for p in self.parameter
            ]


    @classmethod
    def from_string( cls, datapoint: str ) -> 'Datapoint':
        ''' Converts datapoint from '--Inform=<category>;%parameter%'-formatted
        string to Datapoint instance
        '''
        datapoint = MediaInfo.DATAPOINTS.get( datapoint, datapoint ) # Handle shorthands
        try:
            res = re.match( r"^\-\-Inform=(.+?);(.+)$", datapoint ).groups(0)
            assert len(res)==2
            return Datapoint( *res )
        except AttributeError as e:
            raise ValueError(f"Datapoint.from_string : could not find category from datapoint string '{datapoint}'") from e


    @classmethod
    def from_strings( cls, datapoints: Iterable[str] ) -> List['Datapoint']:
        ''' Converts datapoint from '--Inform=<category>;%parameter%'-formatted
        string to Datapoint instance
        '''
        return [
            Datapoint.from_string(dp)
            for dp in datapoints
        ]


    @classmethod
    def group_by_category( cls, datapoints: Iterable['Datapoint'] ) -> Dict[str,List['Datapoint']]:
        ''' Group datapoints by category
        '''
        return {
            cat: [ 
                d
                for d in datapoints
                if d.category == cat
            ]
            for cat in { d.category for d in datapoints }
        }


    @classmethod 
    def combine( cls, datapoints: Iterable['Datapoint'] ) -> List['Datapoint']:
        ''' From an arbitrary amount of datapoints, combines them into
        Datapoints (one per category).
        '''
        categorized_datapoints = Datapoint.group_by_category(datapoints)
        
        return [
            Datapoint( 
                category=cat, 
                parameter=[
                    cat_dp.parameter
                    for cat_dp in cat_datapoints
                ]
            )
            for cat,cat_datapoints in categorized_datapoints.items()
        ]


class MediaInfo:
    ''' Interface for MediaInfo, useful for retrieving info about
    video/audio/image files.

    example : retrieving info for file 'v.mp4'::

        >>> MI = MediaInfo()                        # MediaInfo interface setup 
        >>> f = Path('v.mp4')                       # File path
        >>> MI.get_base_stats( f )                  # Returns dict with basic stats
        >>> MI.get_datapoint( f, 'V_FrameCount' )   # Returns specific stat (uses shorthand)
        >>> MI.get_datapoint( f, '--Inform=Video;%FrameCount%' )   # Equivalent to previous line

    example 2 : retrieving basic and advanced info about 'v.mp4'::

        >>> MI = MediaInfo()                        # MediaInfo interface setup 
        >>> f = Path('v.mp4')                       # File path
        >>> stats = MI.get_base_stats( f )                  # Returns dict with basic stats
        >>> stats = MI.get_datapoints( f, ['V_StreamSize','V_FrameCount','V_UniqueID'], existing_stats=stats ) # Returns specific stats (uses shorthand; update `stats`)
    
    '''

    # collection of shorthand and their MediaInfo-understandable CLI argument counterpart
    # Naming convention : '<category_name_initial>_<parameter_name>'
    DATAPOINTS = {
        'V_StreamSize' : '--Inform=Video;%StreamSize%',
        'V_FrameCount' : '--Inform=Video;%FrameCount%',
        'V_UniqueID'   : '--Inform=Video;%UniqueID%',
        'V_Duration'   : '--Inform=Video;%Duration%',
        'V_FrameRate'  : '--Inform=Video;%FrameRate%'
    }

    UNIT_FACTOR = {
        'Mb/s'    : 1_000_000,
        'kb/s'    : 1000,
        'b/s'     : 1,
        'bits'    : 1,
        'GiB'     : 1_000_000_000,
        'MiB'     : 1_000_000,
        'KiB'     : 1_000,
        'pixels'  : 1,
        'FPS'     : 1,
        'ms'      : 0.001,
        'kHz'     : 1_000,
        'channels': 1
    }

    def __init__( self, executable: str = 'MediaInfo', logLevel: int = logging.WARNING ) -> None:
        ''' `executable` : if typing 'MediaInfo' on a shell doesn't call mediainfo, specify using this argument a valid string that does.
                           It can be a variant (eg. 'mediainfo.exe') or a path (eg. '~/tmp/mediainfo/mediainfo').
        '''
        self.log = logging.getLogger('MediaInfo')
        self.log.setLevel( logLevel )
        self.executable = executable
        type_assert( executable, 'executable', str, 'MediaInfo: ' )
        self.version = None 
        self.get_MI_version()

        self.log.debug("Successfully initialized object : %s" , str(self))


    def get_MI_version( self ) -> None:
        ''' Tries to obtain callable MediaInfo version
        '''
        try:
            stdout = execute(
                command=[self.executable,'--Version']
            )['stdout'].replace('\n', '')
            self.version = re.search( r"(v[\.0-9]+)", stdout ).group(0)
        except AttributeError as e:
            raise ValueError(f"MediaInfo : could not find a version number from string '{stdout}'") from e


    def __str__(self) -> str:
        return f"< Mediainfo : executable '{self.executable}' version '{self.version}' >"


    def __repr__(self) -> str:
        return str(self)


    @classmethod
    def __try_casting_numbers( cls, s: str ) -> MEDIAINFO_POSSIBLE_RETURN_VALUES:
        ''' Simple helper function; tries to cast str -> int/float
        returns argument when fails
        '''
        
        try:
            return int(s)
        except ValueError:
            try:
                return float(s)
            except ValueError:
                return s


    @classmethod
    def __filter_data( cls, s: str ) -> MEDIAINFO_POSSIBLE_RETURN_VALUES:
        ''' MediaInfo typically returns a number. This function handles the conversion 
        process in the case this number includes a unit and a "simple"/"raw" value is
        desired. 
        
        Note that after the conversion the value is passed to `MediaInfo.__try_casting_numbers` 
        for basic int/float conversion.
        '''
        if s in ['','\r\n','\n', None]:
            return None
            
        for unit,mult in cls.UNIT_FACTOR.items():
            pos = s.find( unit )                
            if pos != -1:
                s_ok = re.sub( r'(\d) (\d)', r'\1\2', s[:pos] ) # remove unit and spaces between numbers
                val = MediaInfo.__try_casting_numbers( s_ok )

                if type(val) in [int,float]:
                    # successful cast
                    return val * mult
        
        return MediaInfo.__try_casting_numbers(s)


    def get_base_stats( self, media_file: Path ) -> Dict[str,Dict[str,MEDIAINFO_POSSIBLE_RETURN_VALUES]]:
        ''' Convenience function : retrieves the stats returned by MediaInfo 
        when ran without specific arguments

        WARNING: Some values returned by default by MediaInfo are imprecise 
        or rounded, typically because they are expressed in user-friendly
        units like 'Mb/s', 'GiB', etc

        Returns : <dict[<category_name:str>,<dict[<datapoint_name:str>,<MediaInfo_value>]>]>
        '''
        type_assert( media_file, 'media_file', Path, 'MediaInfo::get_base_stats: ' )
        _file = media_file.resolve()
        stdout = execute( [self.executable, str(_file)] )['stdout']

        if stdout.strip()=='':
            self.log.warning("Could not retrieve data from file %s. Name too long ?", media_file)
            return {}

        # Preprocessing : decoding, splitting lines, regrouping datapoints
        category = 'Uncategorized'
        lines = { category : list() }
        for line in stdout.splitlines():
            
            # Discard empty lines
            if not line:
                continue
                
            # Data lines have ':'
            if ':' in line:
                lines[category].append( line.split(':') )
                continue

            # Category line (?)
            category = line
            lines[category] = list()

        # Return actual data, nicely formatted
        res = {
            category: {
                s_data[0].strip():MediaInfo.__filter_data(s_data[1].strip())
                for s_data in lines[category]
            }
            for category in lines
            if lines[category]
        }

        # cleanup
        cleanup = {
            'Video': {
                'Frame rate': r'([\.0-9]+) \([0-9/]+\) FPS'
            }
        }
        for _category,_cat_rules in cleanup.items():
            if _category not in res:
                continue

            for _datapoint, _datapoint_rule in _cat_rules.items():
                if _datapoint not in res[_category]:
                    continue
                if not isinstance( res[_category][_datapoint], str ):
                    continue

                # apply cleanup regex
                regex_res = re.search(
                    pattern=_datapoint_rule,
                    string=res[_category][_datapoint]
                )
                if regex_res:
                    res[_category][_datapoint] = self.__try_casting_numbers(
                        regex_res[1]
                    )

        return res


    def __get_datapoint( self, media_file: Path, datapoint: Datapoint ) -> MEDIAINFO_POSSIBLE_RETURN_VALUES:
        ''' Calls MediaInfo to get a datapoint value.
        `datapoint` must be in a form understandable by MediaInfo, like '--Inform=Video;%UniqueID%'
        '''

        data = execute( 
            [ 
                self.executable,
                str(datapoint),
                str(media_file)
            ]
        )['stdout']

        if data.strip()=='':
            self.log.warning("Could not retrieve data from file %s. Name too long ?", media_file)
            return None
        
        return data


    def get_datapoint( self, media_file: Path, datapoint: str ) -> MEDIAINFO_POSSIBLE_RETURN_VALUES:
        ''' Gets one datapoint's value
        For multiple datapoints, use `MediaInfo.get_datapoints`

        `datapoint` can be in a shorthand format

        Returns : <dict[<datapoint_name:str>,<MediaInfo_value>]>
        '''
        type_assert( media_file, 'media_file', Path, 'MediaInfo::get_base_stats: ' )
        _file = media_file.resolve()

        # `datapoint` may be a shorthand datapoint reference. ex : 'V_UniqueID' is shorthand for '--Inform=Video;%UniqueID%'
        dp = Datapoint.from_string( self.DATAPOINTS.get( datapoint, datapoint ) )
        return MediaInfo.__filter_data(self.__get_datapoint( _file, dp ))


    def get_datapoints( self, media_file: Path, datapoints: List[str], existing_stats=None ) -> Dict[str,MEDIAINFO_POSSIBLE_RETURN_VALUES]:
        ''' Gets multiple datapoints with as few calls as possible.
        This is done by grouping them by category

        `datapoint` can be in a shorthand format

        `existing_stats`: to update existing stats

        Technical note : MediaInfo supports returning multiple values per call, 
        but this is limited to parameters of the same category.

        Performance note : Internal testing shows that execution time grows linearly
        with the number of calls to `MediaInfo.exec`, therefore using `MediaInfo.get_datapoints`
        is recommended over `MediaInfo.get_datapoints` when more than one datapoint is needed. (TODO: correct note)

        Returns : <dict[<datapoint_name:str>,<MediaInfo_value>]>
        '''
        type_assert( media_file, 'media_file', Path, 'MediaInfo::get_base_stats: ' )
        _file = media_file.resolve()

        # Combine datapoints
        combined_datapoints = Datapoint.combine( 
            Datapoint.from_strings(
                [
                    self.DATAPOINTS.get( dp, dp )
                    for dp in datapoints
                ]
            )
        )
        
        # Issue calls for each combined datapoint, store their result
        res = dict() if existing_stats is None else existing_stats
        for dp in combined_datapoints:
            answer = [
                MediaInfo.__filter_data( dataline )
                for dataline in self.__get_datapoint( _file, dp ).splitlines()
            ]
            nb_answer = len(answer)

            cat = dp.category

            # storing results
            if not cat in res:
                res[cat] = dict()
                
            if isinstance(dp.parameter, str) and nb_answer==1:
                # Datapoint with 1 parameter
                res[cat].update({
                    dp.parameter_shorthand[2:]:answer
                })
                continue

            if nb_answer==len(dp.parameter):
                # Datapoint with N>1 parameters
                res[cat].update({
                    p[2:]:a
                    for p,a in zip( dp.parameter_shorthand, answer )
                })
                continue

            self.log.warning("Illegal state induced by faulty values : datapoint=%s, answer='%s' for file '%s'", dp, answer, media_file)

        return res
