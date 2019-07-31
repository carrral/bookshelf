import unittest
import os
import configparser
import main

CONFIG_FILE = './config/config.ini'
DATA_FILE = './config/bookshelf_data.ini'

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

data = configparser.ConfigParser()
data.read(DATA_FILE)

WORKING_DIR = config.get('DIRECTORIES', 'bookshelf_path')
current_book = data.getint('bookshelf', 'selected_book')

BASE_PATH = config.get('DIRECTORIES', 'base_path')


class TestMain(unittest.TestCase):

    def setUp(self):
        global path
        path = os.path.join(BASE_PATH, WORKING_DIR)

    def test_dir_creation(self):
        main.main()
        path_exists = os.path.exists(path)
        self.assertTrue(path_exists)


if __name__ == '__main__':
    unittest.main()

