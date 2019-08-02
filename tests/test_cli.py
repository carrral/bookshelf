import unittest
import os
import configparser
from bin import cli
import shutil
from config.config import *


class TestMain(unittest.TestCase):

    def setUp(self):
        global path
        path = os.path.join(TEST_MAIN, BOOKSHELF_PATH)
        pass

    def teardown(self):
        shutil.rmtree(path)
        pass

    def test_dir_creation(self):
        path_exists = os.path.exists(path)
        self.assertTrue(path_exists)

    def test_book_creation(self):
        os.system("bookshelf book new -t")
        print(cli.bookshelf.books)
        #book = main.bookshelf.unpickle_book(0)
        #self.assertEqual(book.title, 'Title 1')


if __name__ == '__main__':
    unittest.main()

