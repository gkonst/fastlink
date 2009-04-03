'''
Created on Apr 3, 2009

@author: kostya
'''
import urllib

from util import log

def get_title(url):
    log.debug(" fetching page...")
    message = urllib.urlopen(url)
    content = message.read()
    title = content[content.find('<title>') + len('<title>'):content.find('</title>')]
    charset = message.info().getparam('charset')
    if charset:
        title = title.decode(charset)
    log.debug(" reading page title... : %s", title)
    return title