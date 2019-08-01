import unittest
import os
import configparser
import main
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
        pass


if __name__ == '__main__':
    unittest.main()

