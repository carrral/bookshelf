import os
import configparser
import click
from bookshelf_modules import bookshelf_modules as bs

CONFIG_FILE = './config/config.ini'
DATA_FILE = './config/bookshelf_data.ini'

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

data = configparser.ConfigParser()
data.read(DATA_FILE)

BASE_PATH = config.get('DIRECTORIES', 'base_path')
current_book = data.getint('bookshelf', 'selected_book')

def main():
    book_shelf = bs.Bookshelf(BASE_PATH)


