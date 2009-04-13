'''
Created on Apr 3, 2009

@author: kostya
'''
import urllib

from util import log

ORDER_TAGS_ALPHA = 0
ORDER_TAGS_COUNT = 1
ORDER_POSTS_LAST = 0
ORDER_POSTS_TITLE = 1
ORDER_POSTS_URL = 2

def get_title(url):
    log.debug(" fetching page...")
    message = urllib.urlopen(url)
    content = message.read()
    title = content[content.find('<title>') + len('<title>'):content.find('</title>')]
    charset = message.info().getparam('charset')
    if charset:
        title = title.decode(charset)
    title = title.strip()
    log.debug(" reading page title... : %s", title)
    return title