#!/usr/bin/env python
""" prime.py

    A library of routines to find prime numbers.
    
    When run from the commandline it randomly generates and displays a prime
    number of the size provided by the 'size' argument.
    
    References:
      HAC - "Handbook of Applied Cryptography",Menezes, van Oorschot, Vanstone; 1996
      https://inventwithpython.com/rabinMiller.py 
      http://rosettacode.org/wiki
"""
RABIN_MILLER_ITERATIONS = 40
from os import urandom
import random

def fermat_little_test( p, a ):
    """ Fermat Little Test. Included as a curiosity only.
        p - possible Prime,
        a - any integer
        
        Fermat's Liitle test says that non-primes always have the property that:
        a**(p-1) == 0  mod(p)
    """
    if pow(a,p-1,p) == 1 :
        return True  # could be prime
    else:
        return False  # is NOT prime

def rabin_miller(possiblePrime, aTestInteger):
    """ The Rabin-Miller algorithm to test possible primes
        taken from HAC algorithm 4.24, without the 't' loop
    """
    assert( 1<= aTestInteger <= (possiblePrime-1) ), 'test integer %d out of range for %d'%(aTestInteger,possiblePrime)
    assert( possiblePrime % 2 == 1 ), 'possiblePrime must be odd'
    # calculate s and r such that (possiblePrime-1) = (2**s)*r  with r odd
    r = possiblePrime-1
    s=0
    while (r%2)==0 :
        s+=1
        r=r/2
    y = pow(aTestInteger,r,possiblePrime)
    if ( y!=1 and y!=(possiblePrime-1) ) :
        j = 1
        while ( j <= s-1 and y!=possiblePrime-1 ):
            y = pow(y,2,possiblePrime) #    (y*y) % n
            if y==1 :
                return False # failed - composite
            j = j+1
        if y != (possiblePrime-1):
            return False # failed - composite
    return True          # success, still a possible prime


def is_prime(possible_prime, verbose=False):
    """ Test a number for primality using Rabin-Miller. 
    """
    # prescreen the possible_prime for divisibility by low primes
    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
                  47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                  103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
                  157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                  211, 223, 227, 229, 233, 239, 241, 251, 257):
        if possible_prime % prime == 0:
            if possible_prime == prime:
                return True # for small primes need to check equality
            else:
                if verbose: print("Failed division by: {}".format(prime))
                return False # divisible by small prime from list
                  
    # each successful iteratation 't', the probability of
    # the number being prime increases:  prob = (1-(1/4)**t)
    for iteration in range( RABIN_MILLER_ITERATIONS ):
        witness = random.randrange(2, possible_prime - 1)
        if not rabin_miller(possible_prime, witness):
            if verbose: print("Failed Rabin-Miller iteration: {}".format(iteration))
            return False

    return True


def int_to_string( long_int, padto=None ):
    """ Convert integer long_int into a string of bytes, as per X9.62.
        If 'padto' defined, result is zero padded to this length.
        """
    if long_int > 0:
        octet_string = ""
        while long_int > 0:
            long_int, r = divmod( long_int, 256 )
            octet_string = chr( r ) + octet_string
    elif long_int == 0:
        octet_string = chr(0)
    else:
        raise ValueError('int_to-string unable to convert negative numbers')
    
    if padto:
        padlen = padto - len(octet_string)
        assert padlen >= 0
        octet_string = padlen*chr(0) + octet_string
    return octet_string

def string_to_int( octet_string ):
    """ Convert a string of bytes into an integer, as per X9.62. """
    long_int = 0L
    for c in octet_string:
        long_int = 256 * long_int + ord( c )
    return long_int

def new_random_prime(size_in_bytes, debug=False):
    """ Finds a prime number of close to a specific integer size.
    """
    possible_prime = string_to_int( urandom(size_in_bytes) )
    if not possible_prime % 2:  # even, +1 to make odd
        possible_prime += 1
    
    count = 0
    while True:
        count += 1
        if is_prime( possible_prime, verbose=debug ):
            if debug: print("Prime found after {} attempts.".format(count))
            break
        else:
            possible_prime += 2

    return possible_prime


# -- Command line code, only executed when file is run as 'main'

if __name__ == '__main__':
    import click
    from time import time

    @click.version_option(0.1)

    @click.command(context_settings=dict(help_option_names=['-h', '--help']))
    @click.option('--time', '-t', 'time_flag', is_flag=True, default=False, help='display average time required to generate primes')
    @click.option('--repeat', '-r', default=1, help='create multiple primes')
    @click.option('--debug', '-d', is_flag=True, default=False, help='verbose output of prime generation')
    @click.argument('size', type=int )
    def cli(time_flag, repeat, size, debug):
        """ Generate a prime number of a given SIZE in bytes.
            -r  Repeat generation of prime INTEGER times
            -t  Display average time for prime generation
        """
        start_time = time()
        
        for i in range(repeat):
            p = new_random_prime(size, debug=debug)
        
        stop_time = time()
        avg_time = (stop_time - start_time)/repeat
        
        if repeat == 1:
            click.echo( p )
        
        if time_flag:
            click.echo( "Average time for prime generation of {} bytes is: {}".format(size, avg_time))

    cli()

    

