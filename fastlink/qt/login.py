'''
Created on Apr 1, 2009

@author: kostya
'''
import sys

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialog, QApplication
from PyQt4.QtCore import pyqtSignature

from fastlink.core.util import log
from fastlink.core.config import config 

from fastlink.qt.Ui_login import Ui_Login

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
        if not self.username.text():
            QtGui.QMessageBox.warning(self, "Error", "Username not specified", "Ok")
        elif not self.password.text():
            QtGui.QMessageBox.warning(self, "Error", "Password not specified", "Ok")
        else:
            config.username = str(self.username.text())
            config.password = str(self.password.text())
            log.debug(" login...username : %s, password : %s", config.username, config.password)
            QDialog.accept(self)
        
    def reject(self):
        QApplication.instance().quit()
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            QApplication.instance().quit()