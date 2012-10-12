import operator


def open(lower_value, upper_value):
    '''Helper function to construct an interval object with open lower and upper.

    Example:

    >>> open(100.2, 800.9)
    (100.2, 800.9)
    '''
    return Interval(Interval.OPEN, lower_value, upper_value, Interval.OPEN)


def closed(lower_value, upper_value):
    '''Helper function to construct an interval object with closed lower and upper.

    Example:

    >>> closed(100.2, 800.9)
    [100.2, 800.9]
    '''
    return Interval(Interval.CLOSED, lower_value, upper_value, Interval.CLOSED)


def openclosed(lower_value, upper_value):
    '''Helper function to construct an interval object with a open lower and closed upper.

    Example:

    >>> openclosed(100.2, 800.9)
    (100.2, 800.9]
    '''
    return Interval(Interval.OPEN, lower_value, upper_value, Interval.CLOSED)


def closedopen(lower_value, upper_value):
    '''Helper function to construct an interval object with a closed lower and open upper.

    Example:

    >>> closedopen(100.2, 800.9)
    [100.2, 800.9)
    '''
    return Interval(Interval.CLOSED, lower_value, upper_value, Interval.OPEN)


class Interval:
    '''An interval class with methods associated with mathematical intervals. This class can deal with any comparible objects. 
    
    *Note: comparison is performed solely on the lower value*
    
    Examples
    --------
    An open interval:

    >>> Interval(Interval.OPEN, 100.2, 800.9, Interval.OPEN)
    (100.2, 800.9)
    
    A closed interval:

    >>> Interval(Interval.CLOSED, 100.2, 800.9, Interval.CLOSED)
    [100.2, 800.9]
    
    An open-closed interval:

    >>> Interval(Interval.OPEN, 100.2, 800.9, Interval.CLOSED)
    (100.2, 800.9]
    
    An closed-open interval:

    >>> Interval(Interval.CLOSED, 100.2, 800.9, Interval.OPEN)
    [100.2, 800.9)
    '''
    OPEN = 0
    CLOSED = 1
    
    
    _lower = None
    lower_value = None
    _upper_value = None
    _upper = None
    
    lower_value = property(fget=lambda self: self.lower_value, doc='The intervals lower value')
    upper_value = property(fget=lambda self: self._upper_value, doc='The intervals upper value')
    
    def __init__(self, lower, lower_value, upper_value, upper):
        '''Create a new Interval object, lower and upper should be one of Interval.OPEN or Interval.CLOSED'''
        if lower_value > upper_value:
            raise ValueError('lower_value({lower}) must be smaller than upper_value({upper})'.format(lower=lower_value, upper=upper_value))
        self._lower = lower
        self.lower_value = lower_value
        self._upper_value = upper_value
        self._upper = upper

    def __repr__(self):
        lower_string = '(' if self._lower == self.OPEN else '['
        upper_string = ')' if self._upper == self.OPEN else ']'
        return '{l}{lv}, {uv}{u}'.format(l=lower_string, lv=self.lower_value, uv=self._upper_value, u=upper_string)

    def __lt__(self, other):
        if hasattr(other, 'lower_value'):
            return self.lower_value < other.lower_value
        else:
            raise NotImplementedError
    
    def __le__(self, other):
        if hasattr(other, 'lower_value'):
            return self.lower_value <= other.lower_value
        else:
            raise NotImplementedError
    
    def __eq__(self, other):
        if hasattr(other, '_lower') and hasattr(other, 'lower_value') and hasattr(other, '_upper_value') and hasattr(other, '_upper'):
            return self._lower == other._lower and self.lower_value == other.lower_value and self._upper_value == other._upper_value and self._upper == other._upper
        else:
            raise NotImplementedError
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __gt__(self, other):
        if hasattr(other, 'lower_value'):
            return self.lower_value > other.lower_value
        else:
            raise NotImplementedError
    
    def __ge__(self, other):
        if hasattr(other, 'lower_value'):
            return self.lower_value >= other.lower_value
        else:
            raise NotImplementedError
    
    def __hash__(self):
        return hash(self.lower_value)
    
    def __and__(self, other):
        return self.intersect(self, other)
    
    def __or__(self, other):
        return self.union(self, other)

    def __contains__(self, item):
        g = operator.gt if self._lower is self.OPEN else operator.ge
        l = operator.lt if self._upper is self.OPEN else operator.le
        return g(item, self.lower_value) and l(item, self._upper_value)

    def _get_new_lower_upper(self, other, operator):
        if operator == self.intersect:
            if self.lower_value == other.lower_value:
                new_lower = self._lower and other._lower
            elif self.lower_value < other.lower_value:
                new_lower = other._lower
            else:
                new_lower = self._lower
            
            if self._upper_value == other._upper_value:
                new_upper = self._upper and other._upper
            elif self._upper_value < other._upper_value:
                new_upper = self._upper
            else:
                new_upper = other._upper
        elif operator == self.union:
            if self.lower_value == other.lower_value:
                new_lower = self._lower or other._lower
            elif self.lower_value < other.lower_value:
                new_lower = self._lower
            else:
                new_lower = other._lower
            
            if self._upper_value == other._upper_value:
                new_upper = self._upper or other._upper
            elif self._upper_value < other._upper_value:
                new_upper = other._upper
            else:
                new_upper = self._upper
        return new_lower, new_upper

    def overlaps(self, other):
        '''If self and other have any overlaping values returns True, otherwise returns False'''
        if self.lower_value in other or self._upper_value in other or \
        other.lower_value in self or other._upper_value in self or self == other:
            return True
        return False        
 
    def intersect(self, other):
        if self.overlaps(other):
            newlower_value = max(self.lower_value, other.lower_value)
            new_upper_value = min(self._upper_value, other._upper_value)
            new_lower, new_upper = self._get_new_lower_upper(other, self.intersect)
            return Interval(new_lower, newlower_value, new_upper_value, new_upper)
        else:
            return None

    def union(self, other):
        if self.overlaps(other):
            newlower_value = min(self.lower_value, other.lower_value)
            new_upper_value = max(self._upper_value, other._upper_value)
            new_lower, new_upper = self._get_new_lower_upper(other, self.union)
            return Interval(new_lower, newlower_value, new_upper_value, new_upper)
        else:
            from .interval_set import IntervalSet
            return IntervalSet((self, other))
