'''
Created on Feb 22, 2009

@author: kostya
'''
from Tkinter import *

from delicious.tkinter.widget import ZDialog, ZEntry, ZPasswordEntry
from delicious.core.util import log
import delicious.core.config as config

class Login(ZDialog):
    def __init__(self, master=None):
        ZDialog.__init__(self, master, "Login to Del.icio.us")
    
    def body(self, master):
        master.grid_rowconfigure(0, weight=0, minsize=10, pad=0)
        master.grid_rowconfigure(2, weight=0, minsize=10, pad=0)
        master.grid_rowconfigure(4, weight=0, minsize=10, pad=0)
        self.username = ZEntry(master, label="Username : ", value=config.username)
        self.username.grid(row=1, column=1)
        self.password = ZPasswordEntry(master, label="Password : ", value=config.password)
        self.password.grid(row=3, column=1)
        return self.username
        
    def apply(self):
        config.username = self.username.value()
        config.password = self.password.value()
        log.debug(" login...username : %s, password : %s", config.username, config.password)
