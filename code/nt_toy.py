#!/usr/bin/env python
""" nt_toy.py
    
    Number theory 'toys'.

    Paul A. Lambert, 2017-09-05
"""
import click




# --- 'click' based command-line interface ------------------------------------
@click.version_option(0.1)

@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def cli():
    """ Simple demostrations of number theoretic algorithms. """
    pass


@cli.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument('a', type=int )
@click.argument('p', type=int )
def dlog( a, p):
    """ Try all 'x' for equation: a**x % p == y
    """
    for x in range(1, p+1):
        y = a**x % p
        click.echo("{:>4} **{:>3} % {} == {}".format(a, x, p, y))


@cli.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument('a_max', type=int )
@click.argument('p', type=int )
def dtab( a, p):
    """ Table of values of a**x % p
    """
    #for p in r.... # to be completed   
    #    for x in range(1, p+1):
    #        y = a**x % p
    #       click.echo("{:>4} **{:>3} %{} == {}".format(a, i, p, y)) # fix for table
    pass

if __name__ == '__main__':
    cli()
    

