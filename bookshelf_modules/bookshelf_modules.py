import os
import datetime as dt
import random
import string
import shutil
from config.config import *
from pickle import Pickler, Unpickler

# Class definitions

# Bookshelf class definition


class Bookshelf:
    """Container class for books"""

    def __init__(self, base_path):
        self.base_path = base_path
        self.bookshelf_path = os.path.join(base_path, BOOKSHELF_PATH)

        # Test if bookshelf directory exists
        dir_exists = os.path.exists(self.bookshelf_path)

        if not dir_exists:
            os.mkdir(self.bookshelf_path)

        self.bookshelf_file_path = os.path.join(self.bookshelf_path, ''.join([BOOKSHELF_PATH, BOOKSHELF_FILE_EXT]))

        # Verify that a bookshelf .dump file exists, if not, create one.
        file_exists = os.path.exists(self.bookshelf_file_path)

        if not file_exists:
            self.create_initial_file()

        self.books = self.load_init_list()
        self.book_total = len(self.books)

    def create_initial_file(self):
        """Creates the initial empty list bookshelf/bookshelf.dump file"""
        init_list = list()
        file = open(self.bookshelf_file_path, 'wb')
        pcklr = Pickler(file)
        pcklr.dump(init_list)
        file.close()

    def load_init_list(self):
        file = open(self.bookshelf_file_path, 'rb')
        unpickler = Unpickler(file)
        list_ = unpickler.load()
        file.close()
        return list_

    def pickle_book(self, book, zb_index):
        """Pickles a book in the books' respective directory (zero-based index)"""
        if zb_index not in range(self.book_total):
            raise NonExistentBookException
        else:
            # Generates path src/bookshelf/aAD89k/aAD89k.bk
            dump_path = self.get_book_path(zb_index)
            dump_file_name = ''.join([self.books[zb_index][0], BOOK_FILE_EXT])
            dump_file_path = os.path.join(dump_path, dump_file_name)
            dump_file = open(dump_file_path, "wb")
            pickler = Pickler(dump_file)
            pickler.dump(book)

            # Close file
            dump_file.close()

    def unpickle_book(self, zb_index):
        """Loads a book from a .dump file and returns it"""
        if zb_index not in range(self.book_total):
            raise NonExistentBookException()
        else:
            # Generates load file path src/bookshelf/aAD89k/aAD89k.bk
            _load_file_path = os.path.join(self.get_book_path(zb_index),
                                           ''.join([self.books[zb_index][0], BOOK_FILE_EXT]))
            _load_file = open(_load_file_path, "rb")
            _unpickler = Unpickler(_load_file)

            # Load book
            _loaded_book = _unpickler.load()

            _load_file.close()

            return _loaded_book

    def get_book_list_str(self):
        """Returns a string of the available books in the bookshelf"""
        if self.book_total == 0:
            return "(Empty bookshelf)"

        else:
            titles = [title for dir, title in self.books]
            titles_index = [''.join([str(index + 1), ". ", titles[index]]) for index in range(len(titles))]
            s = "\n".join(titles_index)
            return s

    def get_book_path(self, zb_index):
        """Returns the relative path of a given book"""
        if zb_index not in range(self.book_total):
            raise NonExistentBookException
        else:
            return os.path.join(self.bookshelf_path, self.books[zb_index][0])

    def update_book_title(self, zb_index, new_title):
        if zb_index not in range(self.book_total):
            raise NonExistentBookException()
        else:
            old_tuple = self.books[zb_index]
            new_tuple = (old_tuple[0], new_title)
            self.books[zb_index] = new_tuple

            # Load book
            _current_book = self.unpickle_book(zb_index)
            _current_book.title = new_title

            # Save changes
            self.pickle_book(_current_book, zb_index)

    def new_book(self, title=None):
        """Creates a new book and pickles its initial state"""
        if title is None:
            title = self.generate_automatic_title()

        # Verify there are no matching titles
        if title in [_title for _dir, _title in self.books]:
            raise BookAlreadyExistsException()

        # Generate new directory string
        dir_str = Bookshelf.generate_directory_string(SIZE)

        # Create directory for book
        book_path = os.path.join(self.bookshelf_path, dir_str)
        os.mkdir(book_path)

        # Create new book object
        new_book = Book(title, self.bookshelf_path, dir_str)

        # Append to book list
        self.books.append((dir_str, title))

        # Obtain zero-based index
        zb_index = self.book_total

        # Update book total
        self.book_total += 1

        # Pickle new book
        self.pickle_book(new_book, zb_index)

    def delete_book(self, zb_index):
        """Deletes a book from memory"""

        if self.book_total == 0:
            raise EmptyBookShelfException()

        elif zb_index not in range(self.book_total):
            raise NonExistentBookException()

        # Obtain book path
        path = self.get_book_path(zb_index)

        # Delete directory
        shutil.rmtree(path)

        # Update book list
        self.books.pop(zb_index)
        self.book_total -= 1

    @staticmethod
    def generate_directory_string(n):
        """Generates a random directory string with hexdigits of length n"""
        # TODO Procedurally generate hash value instead of randomly
        # TODO Move method to the driver class
        return "".join([random.choice(string.hexdigits) for i in range(n)])

    def generate_automatic_title(self):
        """Book title generator"""
        title = " ".join(["Book", self.book_total + 1])
        return title


# Book class definition

class Book(object):
    """Container class for entries"""

    def __init__(self, title, bookshelf_path, dir_string):

        # Save current working directory
        self.book_path = os.path.join(bookshelf_path, dir_string)
        self.dir_string = dir_string

        # List of tuples self.entries = [('AFDE32','Entry 1),('EDFESA21','Entry 2')]
        self.entries = list()

        self.entry_total = 0

    def get_entry_file_path(self, zb_index):
        """Returns the relative filepath to a given entry"""

        entry_file = ''.join([self.entries[zb_index][0], ENTRY_FILE_EXT])
        entry_file_path = os.path.join(self.book_path, entry_file)
        return entry_file_path

    def pickle_entry(self, entry, zb_index):
        """Pickles an entry in its corresponding .entry file"""

        # Create entry file
        entry_file_path = self.get_entry_file_path(zb_index)
        file = open(entry_file_path, 'wb')

        # Write to file
        pickler = Pickler(file)
        pickler.dump(entry)

        # Close file
        file.close()

    def unpickle_entry(self, zb_index):
        """Unpickles a picked entry and returns an Entry object"""

        entry_file_path = self.get_entry_file_path(zb_index)
        file = open(entry_file_path, 'rb')
        unpickler = Unpickler(file)
        entry = unpickler.load()

        # Close file
        file.close()

        return entry

    def new_entry(self, title=None, author=AUTHOR):
        """Appends an entry to the entries dictionary and pickles it"""
        if title is None:
            title = self.generate_automatic_title()

        elif title in [t for d, t in self.entries]:
            raise EntryAlreadyExistsException()

        entry_str = Bookshelf.generate_directory_string(SIZE)
        self.entries.append((entry_str, title))
        index = self.entry_total
        new_entry = Entry(author, title, entry_str, self.book_path)
        self.pickle_entry(new_entry, index)
        self.entry_total += 1

    def delete_entry(self, zb_index):
        """Deletes an indexed entry"""
        if self.entry_total == 0:
            raise EmptyBookException()
        else:
            if zb_index not in range(self.entry_total):
                raise NonExistentEntryException("Requested entry does not exists")

            else:
                entry_path = self.get_entry_file_path(zb_index)
                os.remove(entry_path)
                self.entries.pop(zb_index)
                self.entry_total -= 1

    def generate_automatic_title(self):
        # TODO Long date depends on system's language
        now = dt.datetime.now()
        date = now.date().strftime("%A %d/%m/%Y")
        hour = now.time().isoformat("seconds")
        title = " ".join([date, hour])
        return title

    def get_entry_list_str(self):
        if self.entry_total == 0:
            return "(No entries yet)"

        else:
            titles = [title for _dir, title in self.entries]
            titles_index = [''.join([str(index + 1), ". ", titles[index]]) for index in range(len(titles))]
            s = "\n".join(titles_index)
            return s


# Entry class definition
class Entry(object):

    def __init__(self, author, title, entry_str, book_path):
        self.author = author
        self.title = title
        self.filename = Entry.get_entry_body_filepath(entry_str=entry_str, book_path=book_path)
        file = open(self.filename, 'w')
        file.close()
        self.body = None

    def get_entry_header(self):
        # TODO Modify the hardcoded 'Author' for a lenguage-according equivalent
        header = ''' 
    {0}
        
    Author: {1}
        
    '''.format(self.title, self.author)
        return header

    def get_entry_body_vim(self):
        f = open(self.filename, 'a')
        for line in self.get_entry_header().split('\n'):
            f.write(''.join([line[4:], '\n']))
        f.close()
        os.system('vim {0}'.format(self.filename))

    def get_entry_body(self):
        # TODO Native text editing
        if VIM_MODE:
            self.get_entry_body_vim()

    @staticmethod
    def get_entry_body_filepath(book_path, entry_str):
        file_name = ''.join([entry_str, '.txt'])
        txt_filepath = os.path.join(book_path,file_name)
        return txt_filepath


# TODO Encrypted entry class definition
class EncryptedEntry(Entry):
    pass


# Exceptions definition


# Empty containers exception superclass and subclasses
class EmptyContainerException(Exception):
    pass


class EmptyBookShelfException(EmptyContainerException):

    def __init__(self):
        super().__init__("The bookshelf is empty")

    pass


class EmptyBookException(EmptyContainerException):

    def __init__(self):
        super().__init__("Selected book has no entries")


# Non-existent container exception superclass and subclasses
class NonExistentContainerException(Exception):
    pass


class NonExistentEntryException(NonExistentContainerException):
    pass


class NonExistentBookException(NonExistentContainerException):
    def __init__(self):
        super().__init__("Book with given index does not exist")


class BookAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__("This book already exists")


class EntryAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__("An entry with this title already exists")

