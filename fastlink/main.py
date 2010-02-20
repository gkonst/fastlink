import sys

from optparse import OptionParser

from fastlink.core.util import log
from fastlink.core.config import config
    
class Fastlink(object):
    def __init__(self):
        parser = OptionParser()
        parser.add_option("-m", "--mode", dest="mode", default="list", help="Application mode : list or detail")
        parser.add_option("-u", "--ui", dest="ui", default="qt", help="Application ui : tkinter or qt")
        (options, args) = parser.parse_args()
        
        config.configure()
        
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
        import fastlink.tkinter.list as list
        import fastlink.tkinter.detail as detail
        log.debug("Tkinter UI loaded")         
        return (list, detail)

    def _import_qt(self):
        import fastlink.qt.list as list
        import fastlink.qt.detail as detail
        log.debug("QT4 UI loaded")
        return (list, detail)
    
    def _detect_qt(self):
        try:
            import PyQt4
            return True 
        except ImportError:
            return False

    def __del__(self):
        config.save()
    
def start():
    Fastlink()  
