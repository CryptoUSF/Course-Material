#!/usr/bin/env python
""" cipher.py

    A command-line tool implimenting simple ciphers and
    basic frequency analysis tools.
    
    Usage: cipher.py COMMAND [OPTIONS] [ARGS]...
    
    Commands:
        decrypt  Decrypt a file using selected algorithm:...
        dist     Calculate frequency distributions of symbols...
        encrypt  Encrypt a file using selected algorithm:...
        list     List the available ciphers
    
    Help for each command is avaible:
        cipher.py COMMAND -h
        
        
    Example usage:
    
    $./cipher.py encrypt -k none -c caesar ../test_text/midsummers_night.md temp

      caesar cipher encrypted text placed in file 'temp'
    
    $./cipher.py encrypt -k none -c caesar ../test_text/midsummers_night.md temp -
    
      Trigram distribution printed to console ( STDOUT indicated by '-' )
    

    Copyright 2017, Paul A. Lambert
"""
import random
import click
import string

class Cipher(object):
    """ The base class for all Ciphers """
    pass # more here later ... pretty print, naming OIDs etc.

class Simple_Cipher(Cipher):
    """ A Simple Cipher class used to simulate classic ciphers. """
    pt_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" # default unless overloaded

    def preprocess(self, plain_text, remove_whitespace=True):
        """ Translate the plain text into upper case and remove
            unsupported characters.
        """
        pt = []
        for c in plain_text.upper():
            if c in self.pt_alphabet:
                pt.append(c)
            elif c in string.whitespace and not remove_whitespace:
                pt.append(c)
            else:
                pass # skipping characters not found in pt alphabet
        return ''.join(pt)

class Monoalphabetic_Cipher(Simple_Cipher):
    """ A simple monoalphabetic substitution cipher.
        Base class used for decoder badges.
    """
    def __init__(self, key):
        """ This cipher is keyed by providing a string
            indicating the alignment between a symbol
            in the plaintext alphabet with a symbol in the
            cipher text alphabet of the form 'C-G'. The
            cipher text alphabet is then shifted by this
            alignment.
        """
        pta = self.pt_alphabet
        cta = self.ct_alphabet
        
        try:
            pt_key_symbol, ct_symbol = key.split('-')
            assert pt_key_symbol in pta
            assert ct_key_symbol in cta
            height, width = int(h), int(w)
        except:
            raise ValueError( "Illegal key of of '{}' for Monoalphabetic cipher".format(key) )
        # given a postion on the pt_alphabet and the ct_alphabet
        # create a shifted version of the ct_alphabet and form
        # a substitution dictionary for the mono-alphabetic cipher
        pt_key_position = pta.index(pt_key_symbol)
        ct_key_position = cta.index(ct_key_symbol)
        shift = pt_key_position - ct_key_position
        alpha_len = len(cta)
        
        if shift > 0:
            ct_shifted_alphabet = cta[alpha_len - shift:] + cta[0:alpha_len - shift]
        elif shift < 0:
            ct_shifted_alphabet = cta[-shift:] + cta[0:-shift]
        else:
            pass # no shift of ct_alphabet from it's standard representation

        self.encode_dict = dict( zip(pta, ct_shifted_alphabet) )
        self.decode_dict = dict( zip(ct_shifted_alphabet, pta) )

    def encrypt(self, plain_text):
        """ Encrypt a simple substitution cipher.
        """
        pt = self.preprocess(plain_text)
        cipher_text = []

        for symbol in pt:
            cipher_text.append( self.encode_dict[ symbol ] )

        return ''.join(cipher_text)

    def decrypt(self, cipher_text):
        """ Decrypt a simple substitution cipher.
        """
        ct = self.preprocess(cipher_text)
        plain_text = []
        
        for symbol in ct:
            plain_text.append( self.decode_dict[ symbol ] )
        
        return ''.join(plain_text)


class Caesar(Monoalphabetic_Cipher):
    """ Caesar cipher. Shift symbols to right by 3. 
    """
    ct_alphabet = "DEFGHIJKLMNOPQRSTUVWXYZABC"

    def __init__(self, key):
        """ ignore key and directly use ct_alphabet for substitution """
        self.encode_dict = dict(zip(self.pt_alphabet, self.ct_alphabet))
        self.decode_dict = dict(zip(self.ct_alphabet, self.pt_alphabet))


class Caesar2(Monoalphabetic_Cipher):
    """ Caesar cipher. Shift symbols to right by 3.
    """
    encode = "DEFGHIJKLMNOPQRSTUVWXYZABC"
    
    def __init__(self, key):
        """ ignore key and directly use ct_alphabet for substitution """
        self.encode_dict = dict(zip(self.pt_alphabet, self.ct_alphabet))
        self.decode_dict = dict(zip(self.ct_alphabet, self.pt_alphabet))


class CM1955(Monoalphabetic_Cipher):
    """ 1955 Captain Midnight Decoder Badge.
    """
    pt_alphabet = "APZOYNXMWLVKUJTSFREQDICHBG"
    ct_alphabet = [ '1','2','3','4','5','6','7','8',
                    '9','10','11','12','13','14',
                    '15','16','17','18','19','20',
                    '21','22','23','24','25','26']
    
    # tbd ... need to support symbol separators


class Block_Transposition_Cipher(Simple_Cipher):
    """ A block transposition cipher moves the symbols in the plain text
        to other positions within a block of text and can be represented
        as a permutation of the symbols.
        This is a base class and does not define the permutation.
    """
    def encrypt(self, plain_text):
        """ Encrypt using a transposition permutation. """
        pt = self.preprocess(plain_text)
        block_size = len( self.transposition_permutation )
        blocks, remainder = divmod( len(pt), block_size )
        cipher_text = []
        # pad to fill out size of transposition permutation
        if remainder:
            num_pad_chars = block_size - remainder
            pad_chars = []
            for i in range( block_size - remainder ):
                c = random.choice( self.pt_alphabet )
                pad_chars.append(c)
            pt += ''.join(pad_chars)
            blocks += 1

        for b in range(blocks):
            for indx, position in enumerate( self.transposition_permutation ):
                cipher_text.append( pt[ position + b*block_size ] )

        return ''.join(cipher_text)

    def decrypt(self, cipher_text):
        """ Decrypt a transposition permutation by calculating the inverse. """
        block_size = len( self.transposition_permutation )
        blocks, remainder = divmod( len(cipher_text), block_size )
        assert remainder == 0   # should be block aligned
        ip = self.inverse_permutation( self.transposition_permutation )
        plain_text = []

        for b in range(blocks):
            for position in ip:
                plain_text.append( cipher_text[ position + b*block_size ] )

        return ''.join(plain_text)

    def inverse_permutation(self, permutation):
        """ Calculate the inverse of a permutation """
        ip = range( len(permutation) )
        for indx, value in enumerate( permutation ):
            ip[ permutation[value] ] = permutation[ indx ]
        return ip


class Stencil(Block_Transposition_Cipher):
    """ The Stencil cipher transposes symbols in the plaintext
        by the use of a grid with holes cut in a quarter
        of the positions such that in rotating the grid, the
        holes cover new positions for each of the four rotations.

        For the six-by-six example shown in [MoC] the equivent
        permutation in grid form is:

            9  0 18  1 10  2
           19 27  3 28 20 29
           11  4 12  5 30 13
           31 14 21 32 22 33
           15  6 16 23 17  7
           24 34 25  8 26 35

        As a permutation:
           (9,0,18,1,10,2,19,27,3,28,20,29,11,4,12,5,30,13,31,14,21,32,22,33,15,6,16,23,17,7,24,34,25,8,26,35)

        Cipher taken from:
            "Manual of Cryptography", 1911, page 80
            http://marshallfoundation.org/library/wp-content/uploads/sites/16/2014/09/WFFvol05watermark.pdf
    """
    transposition_permutation = (9,0,18,1,10,2,19,27,3,28,20,29,11,4,12,5,30,13,31,14,21,32,22,33,15,6,16,23,17,7,24,34,25,8,26,35)

    def __init__(self, key): pass # key not used, need __init__ here for current cli


class Zigzag(Block_Transposition_Cipher):
    """ The Zigzag cipher transposes symbols in the plaintext
        by first writing the characters down the first column,
        then up the next column, then down the third and
        so forth filling out a grid. The plaintext is made by reading
        the grid rows left-to-right/top-to-bottom.

            0  9 10 19
            1  8 11 18
            2  7 12 17
            3  6 13 16
            4  5 14 15

        This may be represented as a permutation of the symbol locations:

        (0, 9, 10, 19, 1, 8, 11, 18, 2, 7, 12, 17, 3, 6, 13, 16, 4, 5, 14, 15)

        Cipher taken from:
          "Manual of Cryptography", 1911, page 21.
          http://marshallfoundation.org/library/wp-content/uploads/sites/16/2014/09/WFFvol05watermark.pdf
    """
    def __init__(self, key):
        """ Create a 'zigzag' permutation given the height and width of the grid.
            The key is a string of height and width of the grid in the form '9x8'
        """
        try:
            h, w = key.split('x')
            height, width = int(h), int(w)
        except:
            raise ValueError( "Illegal key of of {} for Zigzag transposition cipher".format(key) )

        self.transposition_permutation = range(width * height)
        for x in range(width):
            for y in range(height):
                if x % 2:           # x odd, zig up
                    y_ = height - y - 1
                else:
                    y_ = y          # x even, zig down
                index = y_*width + x
                self.transposition_permutation[index] = x*height + y



#HW2 --------
class Distribution(object):
    """ Base class for analysis routines for symbol distributions.
        Results are dictionary objects with human readable keys.
    """
    def to_readable(self):
        """ Convert dictionary of symbols to readable text """
        pp = []
        for nary in self.result:
            pp.append( "{}: {}\n".format( nary, self.result[nary]))
        return ''.join(pp)


class Ngraph(Distribution):
    """ Looking 'n' symbols at a time, create a dictionary
        of the occurrences of the n-ary string of symbols.
        Default is n=1, a monograph.
    """
    def __init__(self, n=1 ):
        self.n = n

    def analyze(self, text):
        n = self.n
        self.result = {} # results are stored as a dictionary
        for i in range( len(text) - n - 1 ):
            nary = text[ i:i+n ]
            if nary in self.result:
                self.result[nary] += 1
            else:
                self.result[nary] = 1
        return self.result


class Monograph(Distribution):
    def analyze(self, text): self.result = Ngraph( n=1 ).analyze(text)

class Digraph(Distribution):
    def analyze(self, text): self.result = Ngraph( n=2 ).analyze(text)

class Trigraph(Distribution):
    def analyze(self, text): self.result = Ngraph( n=3 ).analyze(text)


# collect all supported ciphers in a dictionary
cipher_list = (Caesar, Stencil, Zigzag) # explicit list of supported ciphers
cipher_name_list = [ Cipher.__name__.lower() for Cipher in cipher_list]
# dictionary of lower case name to Cipher using name introspection of class
cipher_dict = { Cipher.__name__.lower() : Cipher for Cipher in cipher_list }

# collect all distribution routines for cli usage
dist_dict = {'mono':Monograph, 'di':Digraph, 'tri':Trigraph, 'ng':Ngraph}
dist_name_list =[ key for key in dist_dict]

# --- 'click' based command-line interface ------------------------------------
@click.version_option(0.1)

@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.pass_context     # ctx
def cli(ctx):
    """ A tool to encrypt or decrypt a file using simple ciphers. """
    pass

@cli.command()
@click.option('--cipher', '-c', 'cipher_name', type=click.Choice( cipher_name_list ) )
@click.password_option('--key', '-k')
@click.argument('input_file', type=click.File('rb'))
@click.argument('output_file', type=click.File('wb'))
def encrypt(cipher_name, key, input_file, output_file):
    """ Encrypt a file using selected algorithm:
            crypt [OPTIONS] encrypt <in_file> <out_file>
    """
    Cipher = cipher_dict[cipher_name] # instantiate class from dictionary
    cipher = Cipher(key)
    plain_text = input_file.read()

    cipher_text = cipher.encrypt( plain_text )

    output_file.write( cipher_text )
    output_file.write("\n")

@cli.command()
@click.option('--cipher', '-c', 'cipher_name', type=click.Choice( cipher_name_list ) )
@click.password_option('--key', '-k')
@click.argument('input_file', type=click.File('rb'))
@click.argument('output_file', type=click.File('wb'))
def decrypt(cipher_name, key, input_file, output_file):
    """ Decrypt a file using selected algorithm:
            crypt decrypt [OPTIONS] <in_file> <out_file>
             -k   key
             -c   cipher name
    """
    Cipher = cipher_dict[ cipher_name ] # instantiate class from dictionary
    cipher = Cipher( key )
    cipher_text = input_file.read()

    plain_text = cipher.decrypt( cipher_text )

    output_file.write( plain_text )
    output_file.write("\n")

@cli.command()
def list():
    """ List the available ciphers that may be invoked with the -c option.
    """
    click.echo( "The following {} ciphers are supported:".format( len(cipher_list)))
    for cipher in cipher_list:
        base_class_name = cipher.__bases__[0].__name__.replace("_", " ")
        click.echo( "    {} - {}".format( cipher.__name__.lower(),
                                          base_class_name ))


# -- additional CLI for HW2

@cli.command()
@click.option('--dtype', '-d', 'dist_name', type=click.Choice( dist_name_list ) )
@click.argument('input_file', type=click.File('rb'))
@click.argument('output_file', type=click.File('wb'))
def Dist(dist_name, input_file, output_file):
    """ Calculate frequency distributions of symbols in files.
    """
    D = dist_dict[dist_name] # instantiate class from dictionary
    dist = D()
    text = input_file.read()

    dist.analyze(text)

    output_file.write( dist.to_readable() )

if __name__ == '__main__':
    cli()
