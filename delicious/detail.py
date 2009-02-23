'''
Created on Feb 22, 2009

@author: kostya
'''
from Tkinter import *

from widget import ZEntry
from util import log

class BookmarkDetail(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.winfo_toplevel().title("Delicious bookmarks: save a bookmark")
        self.grid()
        self.grid_rowconfigure(0, weight=0, minsize=10, pad=0)
        self.grid_rowconfigure(2, weight=0, minsize=10, pad=0)
        self.grid_rowconfigure(4, weight=0, minsize=10, pad=0)
        self.grid_rowconfigure(6, weight=0, minsize=10, pad=0)
        self.grid_rowconfigure(8, weight=0, minsize=10, pad=0)
        self.grid_columnconfigure(0, weight=0, minsize=20, pad=0)
        self.grid_columnconfigure(2, weight=0, minsize=20, pad=0)
        self.create_widgets()
        
    def create_widgets(self):
        clipboard = self.selection_get(selection="CLIPBOARD")
        log.debug(" detecting clipboard : %s", clipboard)
        if clipboard.startswith("http://"):
            self.url = ZEntry(self, label="Url : ", value=clipboard, width=50, state=DISABLED)
        else:
            self.url = ZEntry(self, label="Url : ", width=50)
            
        self.url.add_listener("<Double-Button-1>", self.on_url_dbl_click)
        
        self.url.grid(row=1, column=1, sticky=W)
        
    def on_url_dbl_click(self, event):
        if self.url["state"] == DISABLED:
            self.url["state"] = NORMAL