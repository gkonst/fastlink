'''
Created on Apr 1, 2009

@author: kostya
'''
import sys

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMainWindow, QApplication
from PyQt4.QtCore import pyqtSignature

from delicious.core.cache import Cache
from delicious.core.util import log
from delicious.core.common import get_title
from delicious.core.config import config
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
        clipboard = unicode(QApplication.clipboard().text())
        log.debug(" detecting clipboard : %s", clipboard)
        if clipboard.startswith("http://"):
            self.url.setText(clipboard)
            self.url.setDisabled(True)
            self.show_url.setEnabled(True)
            self.title.setText(get_title(clipboard))
            self.tags.setFocus()

    @pyqtSignature("")
    def on_show_url_clicked(self):
        self.url.setEnabled(True)
        self.show_url.setDisabled(True)
    
    @pyqtSignature("")
    def on_buttonBox_accepted(self):
        self.cache = Cache()
        self.cache.save_post(unicode(self.url.text()), unicode(self.title.text()), unicode(self.tags.text()))
        QApplication.instance().quit()

    @pyqtSignature("")    
    def on_buttonBox_rejected(self):
        QApplication.instance().quit()
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            QApplication.instance().quit()
