'''
Created on Apr 3, 2009

@author: kostya
'''
import urllib
import re

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
    title_el = re.search('<title>(.*)</title>', content, re.DOTALL and re.IGNORECASE)
    if title_el:
        title = title_el.group(1).strip()
    else:
        title = ''
    charset = message.info().getparam('charset')
    if not charset:
        httpequiv_el = re.search('http-equiv\s*=\s*["\']Content-Type["\']\s*content\s*=\s*["\'].*charset\s*=\s*(.*)["\']', content, re.DOTALL and re.IGNORECASE)
        if httpequiv_el:
            charset = httpequiv_el.group(1).strip()
    log.debug('  page charset : %s', charset)
    if charset:
        title = title.decode(charset)
    title = title.strip()
    log.debug(" reading page title... : %s", title)
    return title