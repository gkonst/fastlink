'''
Created on Apr 1, 2009

@author: kostya
'''

import sys
import webbrowser

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMainWindow, QApplication
from PyQt4.QtCore import pyqtSignature

from fastlink.core.cache import Cache
from fastlink.core.util import log
from fastlink.core.config import config
from fastlink.core.common import *
from fastlink.qt.login import Login 

from fastlink.qt.Ui_list import Ui_BookmarkList

def start_ui():
    app = QApplication(sys.argv)
    wnd = BookmarkList()
    wnd.show()
    sys.exit(app.exec_())

class BookmarkList(QMainWindow, Ui_BookmarkList):
    '''
    classdocs
    '''

    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.login()
        
    def login(self):
        if not config.username or not config.password:
            login = Login(self)
            ret = login.exec_()
            if ret != 0:
                self.fill()
            else:
                sys.exit()
        else:
            self.fill()
            
    def fill(self):
        self.setWindowTitle("Delicious bookmarks : %s" % config.username)
        self.cache = Cache()
        self.refresh_tags()
        self.refresh_posts()                       
        
    def refresh_tags(self, tag=""):
        tags = self.cache.find_tags(tag, self.tags_order.currentIndex())
        self.tagList.clear()
        for item in tags:
            self.tagList.addItem(item[0])
        self.tags_count.setText(str(len(tags)))
        
    def refresh_posts(self, tag="", exact=False):
        self.posts = self.cache.find_posts_by_tag(tag, exact, self.posts_order.currentIndex())
        self.postList.clear()
        for item in self.posts:
            self.postList.addItem(item[0])
        self.posts_count.setText(str(len(self.posts)))
    
    @pyqtSignature("QString")        
    def on_search_textEdited(self, new_text):
        self.refresh_tags(unicode(self.search.text()))
        self.refresh_posts(unicode(self.search.text()))       
        
    @pyqtSignature("")
    def on_tagList_itemSelectionChanged(self):
        if self.tagList.count() != 0:
            tag = str(self.tagList.currentItem().text())
            self.refresh_posts(tag)
            
    @pyqtSignature("int")
    def on_tags_order_currentIndexChanged(self, index):
        self.refresh_tags(unicode(self.search.text()))
        
    @pyqtSignature("int")
    def on_posts_order_currentIndexChanged(self, index):
        if self.tagList.currentItem():
            tag = unicode(self.tagList.currentItem().text())
            self.refresh_posts(tag, True)
        else:
            self.refresh_posts(unicode(self.search.text()))

    @pyqtSignature("QListWidgetItem*")    
    def on_postList_itemDoubleClicked(self, item):
        index = self.postList.currentRow()
        post = self.posts[index]
        log.debug("selected post : %s", post)
        log.debug("goto url : %s", post[1])
        webbrowser.open_new_tab(post[1])
        
    @pyqtSignature("")
    def on_sign_out_triggered(self):
        config.username = None
        config.password = None
        self.login()
        
    @pyqtSignature("")
    def on_about_qt_triggered(self):
         QtGui.QMessageBox.aboutQt(self)
         
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            QApplication.instance().quit()