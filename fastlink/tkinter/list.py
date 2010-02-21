# -*- coding: utf-8 -*-
'''
Bookmark list implementation using **Tkinter** library.

.. moduleauthor:: Konstantin_Grigoriev <Konstantin.V.Grigoriev@gmail.com>
'''
from Tkinter import *
import tkFont
import webbrowser
from threading import Thread
import Queue

from fastlink.core.cache import Cache
from fastlink.core.util import log
from fastlink.tkinter.login import Login
from fastlink.tkinter.widget import ZListBox, ZEntry, ZStatusBar, ZSpinner
from fastlink.tkinter import spinner_image
from fastlink.core.config import config   

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
    
def run_cache_refresh(queue):
    queue.put(Cache().refresh())

class BoormarkList(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.winfo_toplevel().title("Fastlink bookmarks")
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
        self.winfo_toplevel().title('Fastlink bookmarks : %s' % config.username)
        self.cache = Cache()
        self.refresh_tags()
        self.refresh_posts()  
        self.start_cache_refresh()
        
    def start_cache_refresh(self):
        self.queue = Queue.Queue()
        self.refresh()
        self.spinner.show('Synchronizing...')
        Thread(target=run_cache_refresh, args=(self.queue,)).start()
        
    def refresh(self):
        try:
            while 1:
                val = self.queue.get_nowait()
                if val:
                    self.refresh_tags()
                    self.refresh_posts()
                self.spinner.hide()
                self.update_idletasks()
        except Queue.Empty:
            pass
        self.after(100, self.refresh)

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
        self.postList = ZListBox(self, width=60, height=25)
        self.postList.grid(row=5, column=1, sticky=W)
        self.postList.on_row_click(self.tagList.clear_selection)
        self.postList.on_row_dbl_click(self.on_post_dbl_clicked)
        #status bar
        self.status = ZStatusBar(self.master)
        self.status.grid(sticky=W+E)
        #spinner
        self.spinner = ZSpinner(self.status, spinner_image)
        self.spinner.grid()

    def quit(self):
        if self.cache:
            del self.cache
        Frame.quit(self)
        
    def quit_handler(self, event):
        self.quit()
            
    def refresh_tags(self, tag=""):
        tags = self.cache.find_tags(tag)
        self.tagList.set_data(tags, lambda item: item[0])
        
    def refresh_posts(self, pattern="", exact=False):
        if exact:
            self.posts = self.cache.find_posts_by_tag(pattern, exact)
        else:
            self.posts = self.cache.find_posts_by_pattern(pattern)
        self.postList.set_data(self.posts, lambda item: item[0])       
    
    def on_search_changed(self, event):
        self.refresh_tags(self.search.value())
        self.refresh_posts(self.search.value())
        
    def on_tag_clicked(self, event):
        tag = self.tagList.get_current_row()
        self.refresh_posts(tag, exact=True)
        
    def on_post_dbl_clicked(self, event):
        index = self.postList.get_current_index()
        post = self.posts[index]
        log.debug("selected post : %s", post)
        log.debug("goto url : %s", post[1])
        webbrowser.open_new_tab(post[1]) 
        