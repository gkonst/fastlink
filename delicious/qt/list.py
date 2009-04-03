'''
Created on Apr 1, 2009

@author: kostya
'''

import sys
import webbrowser

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMainWindow, QApplication
from PyQt4.QtCore import pyqtSignature

from delicious.core.cache import Cache
from delicious.core.util import log
import delicious.core.config as config
from delicious.core.common import *
from delicious.qt.login import Login 

from delicious.qt.Ui_list import Ui_BookmarkList

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
        if not config.username or not config.password:
            login = Login(self)
            login.setModal(True)
            login.show()
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
        self.refresh_tags(str(self.search.text()))
        self.refresh_posts(str(self.search.text()))       
        
    @pyqtSignature("")
    def on_tagList_itemSelectionChanged(self):
        if self.tagList.count() != 0:
            tag = str(self.tagList.currentItem().text())
            self.refresh_posts(tag)
            
    @pyqtSignature("int")
    def on_tags_order_currentIndexChanged(self, index):
        self.refresh_tags(str(self.search.text()))
        
    @pyqtSignature("int")
    def on_posts_order_currentIndexChanged(self, index):
        if self.tagList.currentItem():
            tag = str(self.tagList.currentItem().text())
            self.refresh_posts(tag, True)
        else:
            self.refresh_posts(str(self.search.text()))

    @pyqtSignature("QListWidgetItem*")    
    def on_postList_itemDoubleClicked(self, item):
        index = self.postList.currentRow()
        post = self.posts[index]
        log.debug("selected post : %s", post)
        log.debug("goto url : %s", post[1])
        webbrowser.open_new_tab(post[1]) 