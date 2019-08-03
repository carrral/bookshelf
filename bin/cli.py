import click
from config import config_script as c_s
from bookshelf_modules import bookshelf_modules as bs

working_bookshelf = bs.Bookshelf(c_s.TEST_MAIN)

# Function definition
@click.group()
def bookshelf(title=None):
    pass


@bookshelf.command(name='new')
@click.argument('element_type', type=click.Choice(['book', 'entry']), required=True)
@click.option('--title', '-t', required=False, type=click.STRING)
@click.option('--author', '-a', required=False, type=click.STRING)
def new(element_type, title=None, author=None):
    if element_type is 'book':
        working_bookshelf.new_book(title)
    else:
        book_ = working_bookshelf.unpickle_book(c_s.current_book)
        book_.new_entry(title, author)


@bookshelf.command(name='list')
def list(elem_type):
    pass






