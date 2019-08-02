import os
import click
from config.config import *
from bookshelf_modules import bookshelf_modules as bs

# Function definition
@click.group()
def bookshelf(title=None):
    _bookshelf = bs.Bookshelf(TEST_MAIN)


@bookshelf.command(name='new')
def new():
    click.echo('libro')


@bookshelf.command()
def entry():
    click.echo('entrada')








