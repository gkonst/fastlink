'''
Created on Feb 21, 2009

@author: kostya
'''
from Tkinter import *
import tkFont
import webbrowser
import sys

from delicious.core.cache import Cache
from delicious.core.util import log
from delicious.tkinter.login import Login
from delicious.tkinter.widget import ZListBox, ZEntry
import delicious.core.config as config   

def start_ui():
    root = Tk()
#        try:
#            root.tk.call('package', 'require', 'tile')
#            root.tk.call('namespace', 'import', '-force', 'ttk::*')
#            root.tk.call('ttk::setTheme', 'clam')
#        except TclError:
#            pass
    BoormarkList(root)
    root.mainloop()

class BoormarkList(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.winfo_toplevel().title("Delicious bookmarks")
        self.winfo_toplevel().bind("<Escape>", self.quit_handler)
        self.grid()
        self.grid_rowconfigure(0, weight=0, minsize=10, pad=0)
        self.grid_rowconfigure(2, weight=0, minsize=10, pad=0)
        self.grid_rowconfigure(4, weight=0, minsize=10, pad=0)
        self.grid_rowconfigure(6, weight=0, minsize=10, pad=0)
        self.grid_rowconfigure(8, weight=0, minsize=10, pad=0)
        self.grid_columnconfigure(0, weight=0, minsize=20, pad=0)
        self.grid_columnconfigure(2, weight=0, minsize=20, pad=0)
        self.createWidgets()
        self.cache = None
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
        self.winfo_toplevel().title("Delicious bookmarks : %s" % config.username)
        self.cache = Cache()
        self.refresh_tags()
        self.refresh_posts()                

    def createWidgets(self):
        self.search = ZEntry(self)
        self.search.add_listener("<KeyRelease>", self.on_search_changed)
        self.search.grid(row=1, column=1, sticky=W)
        self.search.focus()
        #tag list frame
        self.tagList = ZListBox(self)
        self.tagList.grid(row=3, column=1, sticky=W)
        self.tagList.on_row_click(self.on_tag_clicked)
        #post list frame
        self.postList = ZListBox(self, width=60, height=30)
        self.postList.grid(row=5, column=1, sticky=W)
        self.postList.on_row_click(self.tagList.clear_selection)
        self.postList.on_row_dbl_click(self.on_post_dbl_clicked)
        #quit button
        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.grid(row=7, column=1)

    def quit(self):
        if self.cache:
            del self.cache
        Frame.quit(self)
        
    def quit_handler(self, event):
        self.quit()
            
    def refresh_tags(self, tag=""):
        tags = self.cache.find_tags(tag)
        self.tagList.set_data(tags, lambda item: item[0])
        
    def refresh_posts(self, tag="", exact=False):
        self.posts = self.cache.find_posts_by_tag(tag, exact)
        self.postList.set_data(self.posts, lambda item: item[0])       
    
    def on_search_changed(self, event):
        self.refresh_tags(self.search.value())
        self.refresh_posts(self.search.value())
        
    def on_tag_clicked(self, event):
        tag = self.tagList.get_current_row()
        self.refresh_posts(tag)
        
    def on_post_dbl_clicked(self, event):
        index = self.postList.get_current_index()
        post = self.posts[index]
        log.debug("selected post : %s", post)
        log.debug("goto url : %s", post[1])
        webbrowser.open_new_tab(post[1]) 
        