# coding:utf-8
# Standard modules
import requests, os, asyncio,sys,time,shutil
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Modules via Pip
import aiohttp
from bs4 import BeautifulSoup
from ebooklib import epub

# Custom Modules
from auxillary_functions import yomituki
from auxillary_functions import custom_functions

# Browser warnings disabled
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

dirn = os.getcwd()
hd = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'}
proxy = {}
paio = None

fullruby,furigana = True,False
factory = BeautifulSoup('<b></b>', 'lxml')

# Increasing or decreasing changes the download speed
threads = 80


def getpage(link):
    gethtml = requests.get(link, headers=hd, proxies=proxy, verify=False)
    return gethtml

def gettag(word):
    tags = []
    while '〔' in word:
        s = word.find('〔')
        e = word.find('〕')
        tags.append(word[s:e + 1])
        word = word[e + 1:]
    return tags

def correct_point_ruby_as_bold(bs):
    for ruby in bs.find_all('ruby'):
        rt = ruby.find('rt').string.split()[0]
        if rt in '・' * 100:
            rep = factory.new_tag('b')
            rep.string = ruby.find('rb').string.split()[0]
            ruby.replace_with(rep)

def build_page(content, url):
    page = BeautifulSoup(content, 'lxml')
    subtitle = page.find('p', class_="novel_subtitle").get_text()
    content = page.find('div', id="novel_honbun", class_="novel_view")

    # Enable/Disable Furigana
    if furigana:
        correct_point_ruby_as_bold(content)
        if fullruby:
            content = yomituki.ruby_div(content)
        else:
            content = content.prettify()
    else:
        content=content.prettify()

    append = page.find('div', id="novel_a", class_="novel_view")

    if append is not None:
        correct_point_ruby_as_bold(append)
        if fullruby:
            append = yomituki.ruby_div(append)
        else:
            append = append.prettify()
        append = '<hr>' + append
    else:
        append = ''
    html = '<html>\n<head>\n' + '<title>' + subtitle + '</title>\n</head>\n<body>\n<div>\n<h3>' + subtitle + '</h3>\n' + content + append + '</div>\n</body>\n</html>'
    name = url.split('/')[-2]
    built_page = epub.EpubHtml(title=subtitle, file_name=name + '.xhtml', content=html, lang='ja_jp')
    return name, built_page

def build_section(sec):
    head = epub.Section(sec[0])
    main = tuple(sec[1:])
    return head, main

# List of URLS
urlc=list()

# Maximum number of URLS
async def load_page(url, session, semaphore):

    async with semaphore:
        async with session.get(url, proxy=paio) as response:
            content = await response.read()
            urlc.append(url)

            #Progress bar
            progress=len(urlc)/24
            sys.stdout.write(str((custom_functions.update_progress(progress))))
            time.sleep(0.1)

    return url, content


class Novel_Syosetu:
    def __init__(self, novel_id):
        self.id = novel_id
        self.book = epub.EpubBook()
        self.book.set_identifier(self.id)
        self.book.set_language('jp')
        self.book.spine = ['nav']

    def get_meta(self):

        print('[Main Thread] Fetching Metadata...')
        self.metapage_raw = getpage('https://ncode.syosetu.com/' + self.id + '/')
        self.metapage = BeautifulSoup(self.metapage_raw.content, 'lxml')
        self.novel_title = self.metapage.find('title').get_text()
        self.author = self.metapage.find('div', class_="novel_writername").get_text().split('：')[-1][:-1]
        self.about = self.metapage.find("div", id="novel_ex").prettify()
        self.book.set_title(self.novel_title)
        self.book.add_author(self.author)
        self.book.add_metadata('DC', 'description', self.about)
        try:
            self.attention = self.metapage.find('div', class_="contents1").find('span', class_="attention").get_text()
        except AttributeError:
            self.attention = None

    async def get_pages(self):
        print('[Main Thread] Fetching Pages...')
        self.menu_raw = self.metapage.find('div', class_='index_box')
        async with aiohttp.ClientSession(headers=hd) as session:
            tasks = []
            semaphore = asyncio.Semaphore(threads)
            for element in self.menu_raw:
                try:
                    if element['class'] == ['novel_sublist2']:
                        t = element.find('a')
                        url = 'https://ncode.syosetu.com' + t['href']
                        task = asyncio.ensure_future(load_page(url, session, semaphore))
                        tasks.append(task)
                except TypeError:
                    pass
            scheduled = asyncio.gather(*tasks)
            fetch_pages = await scheduled
            self.fetch_pages = {page[0]: page[1] for page in fetch_pages}

    def build_menu(self):
        print('[Main Thread] Building Menu...')
        self.menu = [['メニュー']]
        for element in self.menu_raw:
            try:
                if element['class'] == ['novel_sublist2']:
                    url = 'https://ncode.syosetu.com' + element.find('a')['href']
                    title = element.find('a').string
                    filename, epub_page = build_page(self.fetch_pages[url], url)
                    self.book.add_item(epub_page)
                    self.book.spine.append(epub_page)
                    self.menu[-1].append(epub.Link(filename + '.xhtml', title, filename))
                elif element['class'] == ['chapter_title']:
                    title = element.string
                    if self.menu[-1] == ['メニュー']:
                        self.menu[-1] = [title]
                    else:
                        self.menu.append([title])
            except TypeError:
                pass
        self.book.toc = tuple([build_section(sec) for sec in self.menu])

    def post_process(self):
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())
        self.book.add_item(
                epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=custom_functions.book_style()))

    def build_epub(self):
        print('[Main Thread] Building Book...')
        if len(self.novel_title) > 63:
            self.file_name = self.novel_title[:63]
        else:
            self.file_name = self.novel_title[:63]

        #Moves the created novels into the appropriate directory
        print(dirn+"/novels")
        epub.write_epub(dirn+"/novels_downloaded/"  + self.file_name + '.epub', self.book, {})

        print('[Main Thread] Finished. File saved.')

def syosetu_book_grab():
    '''
    This function is imported into the main module.
    It is for grabbing books from Syosetu
    '''
    while True:
            novel_id = input("Please enter the Link of the book that you would like to download: ")
            code = novel_id.split("com/")
            if r"/ncode.syosetu.com/" in novel_id and len(code)==2:
                syo = Novel_Syosetu(code[1])
                break
            else:
                print("You entered an invalid link. Please try again.\n")

    # Book creation via asyncio
    syo.get_meta()
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(syo.get_pages())
    loop.close()
    syo.build_menu()
    syo.post_process()
    syo.build_epub()
