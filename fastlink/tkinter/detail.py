# -*- coding: utf-8 -*-
'''
Bookmark detail implementation using **Tkinter** library.

.. moduleauthor:: Konstantin_Grigoriev <Konstantin.V.Grigoriev@gmail.com>
'''
from Tkinter import *
from threading import Thread
import Queue

from fastlink.tkinter.widget import ZEntry, ZSplashScreen, ZSuggestion, center_on_screen
from fastlink.core.cache import Cache, SaveException
from fastlink.core.util import log
from fastlink.core.common import get_title
from fastlink.tkinter.login import Login
from fastlink.core.config import config
from fastlink.tkinter import spinner_image

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
        self.winfo_toplevel().title('Fastlink bookmarks: save a bookmark')
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
        self.winfo_toplevel().title('Fastlink bookmarks : %s : save a bookmark' % config.username)
        self.winfo_toplevel().bind("<Escape>", self.quit_handler)
        self.cache = Cache()
        self.tags_suggest.set_find_func(self.cache.find_tags)

    def create_widgets(self):
        try:
            clipboard = self.selection_get(selection="CLIPBOARD")
        except TclError:
            clipboard = ''
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
        self.winfo_toplevel().bind("<Return>", self.save_post)
        box.grid(row=7, column=1)
        self.tags_suggest = ZSuggestion(self.tags, multi=True)

    def on_url_dbl_click(self, event):
        if self.url["state"] == DISABLED:
            self.url["state"] = NORMAL

    def _wait_for_save(self):
        try:
            while 1:
                val = self.queue.get_nowait()
                if 'ERROR' in val:
                    self.splash.hide()
                    import tkMessageBox
                    tkMessageBox.showerror('Error during saving', val)
                else:
                    self.splash.hide()
                    self.update_idletasks()
                    self.quit()
        except Queue.Empty:
            pass
        self.after(100, self._wait_for_save)

    def save_post(self, event=None):
        self.splash = ZSplashScreen(self, image_file=spinner_image)
        self.queue = Queue.Queue()
        self._wait_for_save()
        Thread(target=run, args=(self.queue, self.url.value(), self.title.value(), self.tags.value())).start()
        self.splash.show('Saving...')

    def quit_handler(self, event):
        self.quit()

def run(queue, url, title, tags):
    try:
        Cache().save_post(url, title, tags.strip())
        queue.put('STOP')
    except Exception, e:
        log.exception(e)
        queue.put('ERROR : %s' % e)
