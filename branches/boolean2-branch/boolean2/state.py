"""
Classes to represent state of the simulation
"""

# helps generate a user friendly ID to each state


class State(object):
    """
    Represents a state

    >>> state = State( b=0, c=1)
    >>> state.a = 1
    >>> state
    State: a=1, b=0, c=1
    >>> state.fp()
    'S1'
    >>> state.bin()
    '101'
    """
    MAPPER, COUNTER  = {}, 0

    def __init__(self, **kwds ):
        self.__dict__.update( kwds )
    
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __repr__(self):  
        "Default string format"
        items = [ '%s=%s' % x for x in self.items() ]
        items = ', '.join(items)
        return 'State: %s' % items
   
    def items(self):
        "Returns the sorted keys"
        return sorted( self.__dict__.items() )

    def keys(self):
        "Returns the sorted keys"
        return [ x for x,y in self.items() ]

    def values(self):
        "Returns the values by sorted keys"
        return [ y for x,y in self.items() ]

    def __iter__(self):
        return iter( self.keys() )

    def copy(self):            
        "Duplicates itself"
        s = State( **self.__dict__ )
        return s

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def fp(self):
        "Returns a unique user friendly state definition"
        
        value = hash( str(self) )
        
        if value not in State.MAPPER:
            State.COUNTER += 1
            State.MAPPER[value] = 'S%d' % State.COUNTER

        return State.MAPPER[value]
    
    def bin( self ):
        "A binary representation of the states"
        values = map(str, map(int, self.values()))
        return ''.join(values)

def test():
    """
    Main testrunnner
    """
    # runs the local suite
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    test()
