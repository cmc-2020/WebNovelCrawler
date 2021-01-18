# Syosetsu Web Crawler
from novel_crawlers.syosetu import *


if __name__ == '__main__':
    novel_id = "n2921gf"
    syo = Novel_Syosetu(novel_id)
    syo.get_meta()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(syo.get_pages())
    loop.close()
    syo.build_menu()
    syo.post_process()
    syo.build_epub()