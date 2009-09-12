'''
Created on Feb 22, 2009

@author: kostya
'''
import sys, os
from Tkinter import *
from multiprocessing import Process

from delicious.tkinter.widget import ZEntry, ZSplashScreen, center_on_screen
from delicious.core.cache import Cache
from delicious.core.util import log
from delicious.core.common import get_title
from delicious.tkinter.login import Login
from delicious.core.config import config 

def start_ui():
    root = Tk()
#        try:
#            root.tk.call('package', 'require', 'tile')
#            root.tk.call('namespace', 'import', '-force', 'ttk::*')
#            root.tk.call('ttk::setTheme', 'clam')
#        except TclError:
#            pass
    BookmarkDetail(root)
    root.mainloop()

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
        self.after_idle(center_on_screen, self)
        self.login()
        
    def login(self):
        if not config.username or not config.password:
            Login(self)
            if config.username and config.password:
                self.fill()
            else:
                sys.exit()
        else:
            self.fill()
            
    def fill(self):
        self.winfo_toplevel().title("Delicious bookmarks : %s : save a bookmark" % config.username)
        self.winfo_toplevel().bind("<Escape>", self.quit_handler)
        
    def create_widgets(self):
        clipboard = self.selection_get(selection="CLIPBOARD")
        log.debug(" detecting clipboard : %s", clipboard)
        if clipboard.startswith("http://"):
            self.url = ZEntry(self, label="Url : ", value=clipboard, width=50, state=DISABLED)
            self.title = ZEntry(self, label="Title : ", value=get_title(clipboard), width=50)
        else:
            self.url = ZEntry(self, label="Url : ", width=50)
            self.title = ZEntry(self, label="Title : ", width=50)           
        self.url.add_listener("<Double-Button-1>", self.on_url_dbl_click)
        self.url.grid(row=1, column=1)
        self.title.grid(row=3, column=1)
        self.tags = ZEntry(self, label="Tags : ", width=50)
        self.tags.grid(row=5, column=1)
        self.tags.focus()
        box = Frame(self)
        w = Button(box, text="Save", command=self.save_post, width=10, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", command=self.quit, width=10)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.save_post)
        self.bind("<Escape>", self.quit)
        box.grid(row=7, column=1)
                
    def on_url_dbl_click(self, event):
        if self.url["state"] == DISABLED:
            self.url["state"] = NORMAL

    def save_post(self):
        splash = ZSplashScreen(self, image_file=os.path.join(sys.path[0], 'delicious/images/spinner_%d.gif'))
        Process(target=run, args=(splash.queue, self.url.value(), self.title.value(), self.tags.value())).start()
        splash.start_splash()
        
    def quit_handler(self, event):
        self.quit()

def run(queue, url, title, tags):
    cache = Cache()    
    cache.save_post(url, title, tags)
    queue.put('STOP')