import os
import base64
import ConfigParser
from Tkinter import Tk
from _tkinter import TclError

from list import BoormarkList
from detail import BookmarkDetail
from util import log
import config
    
class Delicious(object):
    def __init__(self):
        home_dir = os.path.expanduser("~")
        config.config_dir = os.path.join(home_dir, ".delicious")
        if not os.path.exists(config.config_dir) or not os.path.isdir(config.config_dir):
            os.mkdir(config.config_dir)
        
        if os.path.exists(os.path.join(config.config_dir, "config")):
            config_parser = ConfigParser.RawConfigParser()
            config_parser.read(os.path.join(config.config_dir, "config"))
            if config_parser.has_option("main", "username"):
                config.username = config_parser.get("main", "username")
                log.debug("loading username from config : %s", config.username)
            if config_parser.has_option("main", "password"):
                config.password = self.decrypt_password(config_parser.get("main", "password"))
                log.debug("loading password from config : %s", config.password)
        
        root = Tk()
#        try:
#            root.tk.call('package', 'require', 'tile')
#            root.tk.call('namespace', 'import', '-force', 'ttk::*')
#            root.tk.call('ttk::setTheme', 'clam')
#        except TclError:
#            pass
#        BoormarkList(root)
        BookmarkDetail(root)
        root.mainloop()    
    
    def __del__(self):
        log.debug("saving config...")
        config_parser = ConfigParser.RawConfigParser()
        config_parser.add_section("main")
        if config.username:
            config_parser.set("main", "username", config.username)
        if config.password:
            config_parser.set("main", "password", self.crypt_password(config.password))
        fo = open(os.path.join(config.config_dir, "config"), "w")
        config_parser.write(fo)
        fo.close()
        log.debug("saving config...Ok")
        
    def crypt_password(self, password):
        return base64.b64encode(password)
    
    def decrypt_password(self, password):
        return base64.b64decode(password)
    
def main():
    Delicious()  
    
if __name__ == '__main__':
    main()
