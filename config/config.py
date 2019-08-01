import configparser

CONFIG_FILE = './config/config.ini'
BOOKSHELF_DATA = './config/bookshelf_data.ini'

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

bookshelf_data = configparser.ConfigParser()
bookshelf_data.read(BOOKSHELF_DATA)

TESTING_DIRECTORY = config['test']['test_dir']
TEST_MAIN = config.get('test','test_main')
current_book = bookshelf_data.getint('bookshelf', 'selected_book')
BASE_PATH = config.get('DIRECTORIES', 'base_path')
SIZE = config.getint('DIRECTORIES', 'dir_str_size')
BOOKSHELF_PATH = config.get('DIRECTORIES', 'bookshelf_path')
BOOKSHELF_FILE_EXT = config['file_ext']['bookshelf']
BOOK_FILE_EXT = config['file_ext']['book']
ENTRY_FILE_EXT = config['file_ext']['entry']
AUTHOR = config['info']['author']
VIM_MODE = config['mode']['vim_mode']

