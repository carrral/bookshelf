import unittest
from bookshelf_modules import bookshelf_modules as bs
import os
import shutil
from config.config import *


class BookshelfTest(unittest.TestCase):

    def setUp(self):
        global bookshelf, book
        bookshelf = bs.Bookshelf(TESTING_DIRECTORY)
        bookshelf.new_book('Title')

    def tearDown(self):
        shutil.rmtree(os.path.join(TESTING_DIRECTORY, 'bookshelf'))
        pass

    def test_dir_created(self):
        self.assertTrue(os.path.exists(os.path.join(TESTING_DIRECTORY, 'bookshelf')))

    def test_dumpfile_created(self):
        self.assertTrue(os.path.join(TESTING_DIRECTORY, 'bookshelf/bookshelf.dump'))

    def test_book_list_creation(self):
        self.assertTrue(isinstance(bookshelf.books, list))

    def test_no_repetitions(self):
        self.assertRaises(bs.BookAlreadyExistsException, bookshelf.new_book, 'Title')

    def test_book_persistence(self):
        bookshelf.update_book_title(0, 'New Title')
        unpickled_book = bookshelf.unpickle_book(0)
        self.assertEqual(unpickled_book.title, 'New Title')
        self.assertEqual(unpickled_book.dir_string, bookshelf.books[0][0])


class BookTest(unittest.TestCase):

    def setUp(self):
        global bookshelf, book_1, book_2
        bookshelf = bs.Bookshelf(TESTING_DIRECTORY)
        bookshelf.new_book('Foo')
        bookshelf.new_book('Bar')

        book_1 = bookshelf.unpickle_book(0)  # Foo
        book_2 = bookshelf.unpickle_book(1)  # Bar

    def tearDown(self):
        shutil.rmtree(os.path.join(TESTING_DIRECTORY, 'bookshelf'))

    def test_correct_book_dir(self):
        path = os.path.join(TESTING_DIRECTORY, 'bookshelf', book_1.dir_string)
        self.assertEqual(path, book_1.book_path)

    def test_repeated_entry(self):
        book_1.entries.append(('dir_str', 'Entry'))
        self.assertRaises(bs.EntryAlreadyExistsException, book_1.new_entry, 'Entry')

    def test_entry_file_creation(self):
        book_1.new_entry()
        entry_dir_str = book_1.entries[0][0]
        entry_file_path = os.path.join(book_1.book_path,''.join([entry_dir_str, '.entry']))
        file_exists = os.path.exists(entry_file_path)
        self.assertTrue(file_exists)

    def test_entry_persistence(self):
        book_1.new_entry(title='Titulo 1',author='Autor')
        unpickled_entry = book_1.unpickle_entry(0)
        self.assertEqual('Titulo 1', unpickled_entry.title)
        self.assertEqual('Autor', unpickled_entry.author)

    def test_entry_creation(self):
        book_1.new_entry('Apuntes de git')
        entry = book_1.unpickle_entry(0)
        self.assertEqual(entry.title, 'Apuntes de git')

    def test_entry_deletion(self):
        book_1.new_entry('God is dead')
        self.assertEqual(book_1.entry_total, 1)
        path = book_1.get_entry_file_path(0)
        self.assertTrue(os.path.exists(path))
        book_1.delete_entry(0)
        self.assertTrue(not os.path.exists(path))

    def test_no_repeated_titles(self):
        book_1.new_entry('Yet another entry')
        self.assertRaises(bs.EntryAlreadyExistsException, book_1.new_entry, 'Yet another entry')

    def test_nonexistent_entry(self):
        self.assertRaises(bs.EmptyBookException, book_1.delete_entry, 100)

    def test_generate_entry_list(self):
        book_1.new_entry()
        book_1.new_entry('Yet another entry', author='AMLO')
        # print("\n")
        # print(book_1.get_entry_list_str())
        # print('\n')
        self.assertTrue(True)

    def test_entry_header_string(self):
        book_1.new_entry('This is the header of a new entry')
        entry = book_1.unpickle_entry(0)
        # print(entry.get_entry_header())

    def test_get_entry_body(self):
        book_1.new_entry()
        entry = book_1.unpickle_entry(0)
        # print(entry.get_entry_header())
        # entry.get_entry_body()

        self.assertTrue(True)  # passed



if __name__ == '__main__':
    unittest.main()

