from WebNovelCrawler.debuging.syosetu18 import *
import asyncio


def book_grab():
    novel_id = "n0649go"
    syo = Novel_Syosetu(novel_id)
    syo.get_meta()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(syo.get_pages())
    loop.close()
    syo.build_menu()
    syo.post_process()
    syo.build_epub()

book_grab()