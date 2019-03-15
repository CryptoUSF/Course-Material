#!/usr/bin/env python
""" hash.py
    
    A command-line tool to generate a hash value for a file.
    
    Paul A. Lambert, 2017
"""
import hashlib
from base64 import standard_b64encode, urlsafe_b64encode
import click

# named secure hashes supported by Python 'hashlib'
hash_name_list = ( 'md4',
                   'md5',
                   'ripemd160',
                   'sha',
                   'sha1',
                   'sha224',
                   'sha256',
                   'sha384',
                   'sha512' )

# named encoding formats
encoding_name_list = ( 'hex',
                       'bin',
                       'b64',
                       'b64u')

# -- Command line code, executed when file is run as 'main'
@click.version_option(0.1)
    
@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--algorithm', '-a', 'hash_name', default='sha256',
              type=click.Choice( hash_name_list ),
              help="Specify hash algorithm (default=sha256)")
@click.option('--encoding', '-e', default='hex',
              type=click.Choice( encoding_name_list ),
              help="Select encoding format for hash value")
@click.option('--output_file', '-o', default='-',
              type=click.File('wb'),
              help="Output file, default SDOUT")
@click.argument('input_file', type=click.File('rb'))
def cli(hash_name, encoding, output_file, input_file):
    """ Generate the hash value for a file.
    """
    h = hashlib.new(hash_name)
    file_chunk_size = h.digest_size
    
    while True:
        chunk = input_file.read(file_chunk_size)
        if not chunk:
            break
        h.update( chunk )

    # encode hash value per encoding option
    if encoding == 'hex':
        hash_out = h.hexdigest()
    elif encoding == 'bin':
        hash_out = h.digest()
    elif encoding == 'b64':
        hash_out = standard_b64encode( h.digest() )
    elif encoding == 'b64u':
        hash_out = urlsafe_b64encode( h.digest() )
    else:
        raise ValueError("Bad encoding option") # should not reach here with click

    hashout = hash_out + "\n"
    output_file.write( hash_out )


if __name__ == '__main__':
    cli()
