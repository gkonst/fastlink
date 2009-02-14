import time

from pydelicious import DeliciousAPI

from dao import DAO
from util import log

sync_timeout = 30

class Cache(object):
    
    def __init__(self, username, password):
        log.debug("opening cache...")
        self.dao = DAO()
        self.username = username
        self.password = password
        self.api = DeliciousAPI(self.username, self.password)
        log.debug("opening cache...Ok")
    
    def refresh(self):
        last_sync = self.dao.get_last_sync()
        log.debug(" cache last_sync : %s", last_sync)
        if not last_sync or last_sync and time.time() - float(last_sync) > sync_timeout:
            last_update_in_cache = self.dao.get_last_update()
            ttt = self.api.posts_update()
            last_update = time.strftime("%a, %d %b %Y %H:%M:%S +0000", ttt["update"]["time"])
            log.debug(" last_update : %s, in cache : %s", last_update, last_update_in_cache)
            if(last_update != last_update_in_cache):
                log.debug("refreshing cache...")
                self._refresh_tags()
                self._refresh_posts()
                self.dao.update_last_update(last_update)
                self._update_last_sync()
                log.debug("refreshing cache...Ok")
        
    def _refresh_tags(self):
        tags = self.api.tags_get()['tags']
        self.dao.update_tags(tags)

    def _refresh_posts(self):
        posts = self.api.posts_all()['posts']
        self.dao.update_posts(posts)
        
    def _update_last_sync(self):
        self.dao.update_last_sync(time.time())

def main():
    cache = Cache("Konstantin_Grigoriev", "parabolla_84")
    cache.refresh()
    
if __name__ == '__main__':
    main()