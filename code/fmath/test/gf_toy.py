#!/usr/bin/env python
""" gf_toy.py
    
    Copyright Paul A. Lambert 2017
  
"""
import random

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))   
    from galoisfield import GFp
else:
    from ..galoisfield import GFp

class curve(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def y(self, x):
        y**2 == x**3 + a*x + b

    @classmethod
    def y_from_x(cls, x):
        """ Returns one of the two possible values for y from x.
            Used for point decompression.
            """
        a = cls.a; b = cls.b; p = cls.p
        y_squared = ((x*x+ a)*x + b ) % p
        # it might be y or p - y
        y = square_root_mod_prime( y_squared, p )
        return y


def main():


        
if __name__ == '__main__':
    main()


    

    
 
