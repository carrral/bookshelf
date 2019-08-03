import click
from config.config import *
from bookshelf_modules import bookshelf_modules as bs

working_bookshelf = bs.Bookshelf(TEST_MAIN)

# Function definition
@click.group()
def bookshelf(title=None):
    pass


@bookshelf.command(name='new')
@click.argument('element', type=click.Choice(['book', 'entry']), required=True)
@click.option('--title', '-t')
def new(element, title=None):
    if element == 'book':
        click.echo('libro {}'.format(title))
    else:
        click.echo('entrada {}'.format(title))


@bookshelf.command(name='list')
def list(elem_type):
    pass






