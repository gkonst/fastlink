'''
Created on Apr 1, 2009

@author: kostya
'''
import sys
import urllib

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMainWindow, QApplication
from PyQt4.QtCore import pyqtSignature

from delicious.core.cache import Cache
from delicious.core.util import log
import delicious.core.config as config
from delicious.qt.login import Login 

from delicious.qt.Ui_detail import Ui_BookmarkDetail

def start_ui():
    app = QApplication(sys.argv)
    wnd = BookmarkDetail()
    wnd.show()
    sys.exit(app.exec_())

class BookmarkDetail(QMainWindow, Ui_BookmarkDetail):
    '''
    classdocs
    '''

    def __init__(self, parent = None):
        '''
        Constructor
        '''
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        if not config.username or not config.password:
            login = Login(self)
            login.setModal(True)
            login.show()
        self.setWindowTitle("Delicious bookmarks : %s : save a bookmark" % config.username)
        clipboard = str(QApplication.clipboard().text())
        log.debug(" detecting clipboard : %s", clipboard)
        if clipboard.startswith("http://"):
            self.url.setText(clipboard)
            self.url.setDisabled(True)
            self.title.setText(self.get_title(clipboard))
            self.tags.setFocus()

    @pyqtSignature("")
    def on_url_dbl_click(self, event):
        if self.url["state"] == DISABLED:
            self.url["state"] = NORMAL
            
    def get_title(self, url):
        log.debug(" fetching page...")
        content = urllib.urlopen(url).read()
        log.debug(" reading page title...")
        return content[content.find('<title>') + len('<title>'):content.find('</title>')]
    
    @pyqtSignature("")
    def on_buttonBox_accepted(self):
        self.cache = Cache()
        self.cache.save_post(str(self.url.text()), str(self.title.text()), str(self.tags.text()))
        QApplication.instance().quit()

    @pyqtSignature("")    
    def on_buttonBox_rejected(self):
        QApplication.instance().quit()
