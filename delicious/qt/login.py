'''
Created on Apr 1, 2009

@author: kostya
'''
import sys

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialog, QApplication
from PyQt4.QtCore import pyqtSignature

from delicious.core.util import log
import delicious.core.config as config 

from delicious.qt.Ui_login import Ui_Login

class Login(QDialog, Ui_Login):
    '''
    classdocs
    '''

    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
    
    def accept(self):
        config.username = self.username.value()
        config.password = self.password.value()
        log.debug(" login...username : %s, password : %s", config.username, config.password)
        QDialog.accept(self)
        
    def reject(self):
        QApplication.instance().quit()