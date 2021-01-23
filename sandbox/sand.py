import ebooklib
from ebooklib import epub

book = epub.read_epub('test.epub')

for doc in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
    print (doc)