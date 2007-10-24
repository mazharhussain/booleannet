import math

def choose( p1, p2, t):
    "Every ten seconds chooses p2"
    
    mult = math.floor( t / 10.0)
    t = t - 10 * mult 

    if 7 < t < 9:
        return p2
    else:
        return p1
