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

from delicious.qt.Ui_list import Ui_BoormarkList

def start_ui():
    app = QApplication(sys.argv)
    wnd = BoormarkList()
    wnd.show()
    sys.exit(app.exec_())

class BoormarkList(QMainWindow, Ui_BoormarkList):
    '''
    classdocs
    '''

    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
#        if not config.username or not config.password:
#            Login(self)
#        self.winfo_toplevel().title("Delicious bookmarks : %s" % config.username)
        self.cache = Cache()
        self.refresh_tags()
        self.refresh_posts()
        
    def refresh_tags(self, tag=""):
        tags = self.cache.find_tags(tag)
        self.tagList.clear()
        for item in tags:
            self.tagList.addItem(item[0])
        
    def refresh_posts(self, tag="", exact=False):
        self.posts = self.cache.find_posts_by_tag(tag, exact)
        self.postList.clear()
        for item in self.posts:
            self.postList.addItem(item[0])
    
    @pyqtSignature("QString")        
    def on_search_textEdited(self, new_text):
        self.refresh_tags(str(self.search.text()))
        self.refresh_posts(str(self.search.text()))       
        
    @pyqtSignature("")
    def on_tagList_itemSelectionChanged(self):
        if self.tagList.count() != 0:
            tag = str(self.tagList.currentItem().text())
            self.refresh_posts(tag)

    @pyqtSignature("QListWidgetItem*")    
    def on_postList_itemDoubleClicked(self, item):
        index = self.postList.currentRow()
        post = self.posts[index]
        log.debug("selected post : %s", post)
        log.debug("goto url : %s", post[1])
        webbrowser.open_new_tab(post[1]) 