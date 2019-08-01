import os
import click
from config.config import *
from bookshelf_modules import bookshelf_modules as bs

# Main Program
bookshelf = bs.Bookshelf(TEST_MAIN)
print('PATH (main):{}'.format(bookshelf.bookshelf_path))



