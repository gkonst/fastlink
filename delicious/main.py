import os
import sys
import base64
import ConfigParser
from optparse import OptionParser

from delicious.core.util import log
import delicious.core.config as config
    
class Delicious(object):
    def __init__(self):
        parser = OptionParser()
        parser.add_option("-m", "--mode", dest="mode", default="list", help="Application mode : list or detail")
        parser.add_option("-u", "--ui", dest="ui", default="qt", help="Application ui : tkinter or qt")
        (options, args) = parser.parse_args()
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
        
        if options.ui == "tkinter":
            (list, detail) = self._import_tkinter()
        elif options.ui == "qt":            
            if self._detect_qt():
                (list, detail) = self._import_qt()
            else:
                log.warn("QT4 not found -> using Tkinter")
                (list, detail) = self._import_tkinter()
        else:
            log.error("Unknown ui : %s", options.ui)
            sys.exit() 
                        
        if options.mode == "list":  
            list.start_ui()
        elif options.mode == "detail":  
            detail.start_ui()
        else:
            log.error("Unknown mode : %s", options.mode)
            sys.exit()
            
    def _import_tkinter(self):
        import delicious.tkinter.list as list
        import delicious.tkinter.detail as detail
        log.debug("Tkinter UI loaded")         
        return (list, detail)

    def _import_qt(self):
        import delicious.qt.list as list
        import delicious.qt.detail as detail
        log.debug("QT4 UI loaded")
        return (list, detail)
    
    def _detect_qt(self):
        try:
            import PyQt4
            return True 
        except ImportError:
            return False        
    
    def __del__(self):
        if config.config_dir:
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
    
def start():
    Delicious()  
