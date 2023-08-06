# module-level docstring
__doc__='''
Interval representation implementation
======================================

A simple implementation for generic intervals.
'''


from typing import NewType, Union, Optional, Tuple

Numerical = NewType( 'Numerical', Union[float,int] )

class Interval:
    ''' Represents an interval [a,b] of real (numerical) values
    Note : the interval [a,b] must be strictly positive (a<b)
    '''

    class InvalidInterval(Exception):
        ''' Trivial exception for invalid interval '''
        
    # Needed for visibility
    InvalidInterval=InvalidInterval

    def __init__( self, a: Numerical, b: Numerical, boundary: Optional['Interval'] = None ) -> None:
        assert a<b, f"Interval.__init__: invalid arguments : a={a}, b={b} do not respect rule a<b"
        self.a = a
        self.b = b
        if isinstance(boundary, Interval):
            self.a, self.b = self.intersection( boundary )      

    @property
    def len(self) -> Numerical:
        ''' Property. Represents the length of the interval '''
        return self.b - self.a

    def __str__( self ):
        return f"<Interval {self.a:.2f}-{self.b:.2f} [{self.len:.2f}]>"

    def intersection( self, other: 'Interval', return_obj: bool = False, raise_exception: bool = True ) -> Union['Interval',Tuple[Numerical,Numerical], None]:
        ''' Computes the intersection between two Interval objects.
        Let [x,y] be the valid strictly interval representing the intersection (only exists on
        strictly overlapping intervals).
        
        Returns : either an Interval object representing the [x,y] interval (if `return_obj`),
        or the (x,y) tuple (if not `return_obj`), or nothing if [x,y] doesn't exist 
        (see `raise_exception` below).
        
        `raise_exception` : allows to disable raising exception, returning None instead.
        '''
        assert isinstance( other, Interval )
        a = self.a if other.a < self.a else other.a
        b = self.b if self.b < other.b else other.b
        if b <= a and raise_exception:
            # non-strictly overlapping intervals 
            raise self.InvalidInterval()
        else:
            # valid intersection exists 
            return Interval(a,b) if return_obj else (a, b)

    @classmethod
    def from_length( cls, length: Numerical, start: Optional[Numerical] = None, end: Optional[Numerical] = None ) -> 'Interval':
        ''' Creates an Interval from 2 (or more) of an interval's properties : start point, end point, length '''
        assert 0 < length
        if start:
            if end:
                assert abs((end - start) - length) < (end - start) * 0.01, "Interval.from_length: argument mismatch"
            else:
                end = start + length
        elif end:
            start = end - length
        return Interval( start, end )
        