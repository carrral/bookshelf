import unittest
from click.testing import CliRunner
import os
from bin.cli import working_bookshelf,bookshelf
import shutil
from config.config import *


class TestMain(unittest.TestCase):

    def setUp(self):
        global path,runner
        runner = CliRunner()
        path = os.path.join(TEST_MAIN, BOOKSHELF_PATH)

    def teardown(self):
        #shutil.rmtree(path+'/bookshelf.bs')
        pass

    def test_dir_creation(self):

        path_exists = os.path.exists(path+'/bookshelf.bs')
        self.assertTrue(path_exists)

    def test_book_creation(self):
        runner.invoke(bookshelf, ['new', 'book', '-t "Foo Bar"'])




if __name__ == '__main__':
    unittest.main()

