import time
import os

import pydelicious
from pydelicious import DeliciousAPI, DLCS_WAIT_TIME

from dao import DAO
from util import log

sync_timeout = 30

class Cache(object):
    
    def __init__(self, username, password):
        log.debug("opening cache...")
        self.dao = DAO()
        self.username = username
        self.password = password
        pydelicious.DEBUG = 0
        pydelicious.Waiter = _FileWaiter(DLCS_WAIT_TIME, "pydelicious.stamp")       
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
        
    def find_posts_by_tag(self, tag, exact):
        return self.dao.find_posts_by_tag(tag, exact)
    
    def findTags(self, pattern):
        return self.dao.findTags(pattern)

class _FileWaiter:
    """Waiter makes sure a certain amount of time passes between
    successive calls of `Waiter()`.

    Some attributes:
    :last: time of last call
    :wait: the minimum time needed between calls
    :waited: the number of calls throttled

    pydelicious.Waiter is an instance created when the module is loaded.
    """
    def __init__(self, wait, stamp_file):
        self.wait = wait
        self.waited = 0
        self.stamp_file = stamp_file
        if not os.path.exists(self.stamp_file):
            if pydelicious.DEBUG>0: print "Creating stamp in : ", self.stamp_file 
            fin = open(self.stamp_file, "wt")
            fin = open(self.stamp_file, "rt")
        else:
            if pydelicious.DEBUG>0: print "Using stamp in : ", self.stamp_file
            fin = open(self.stamp_file, "rt")
        content = fin.read()
        if not content:
            self.lastcall = 0
            fin = open(self.stamp_file, "wt")
            fin.write(str(self.lastcall))
        else:
            self.lastcall = float(content)
        fin.close()        

    def __call__(self):
        tt = time.time()
        wait = self.wait

        timeago = tt - self.lastcall
        if pydelicious.DEBUG>0: print "prev : ", self.lastcall, " cur : ", tt, " ago : ", timeago, " wait : ", wait
        if timeago < wait:
            wait = wait - timeago
            if pydelicious.DEBUG>0: print  "Waiting %s seconds." % wait
            time.sleep(wait)
            self.waited += 1
            self._update(tt + wait)
        else:
            self._update(tt)
    
    def _update(self, lastcall):
        self.lastcall = lastcall
        fin = open(self.stamp_file, "wt")
        fin.write(str(lastcall))
        fin.close()

def main():
    cache = Cache("Konstantin_Grigoriev", "parabolla_84")
    cache.refresh()
    
if __name__ == '__main__':
    main()