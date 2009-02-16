from cache import Cache

from pydelicious import DeliciousAPI
    
from Tkinter import *
import tkFont
import webbrowser

class DiliciousApplication(Frame):
    def __init__(self, master=None):
        webuser = "Konstantin_Grigoriev"
        webpass = "parabolla_84"
        self.cache = Cache(webuser, webpass)
        Frame.__init__(self, master)
        self.grid()
        self.grid_rowconfigure(0, weight = 0, minsize = 10, pad = 0)
        self.grid_rowconfigure(2, weight = 0, minsize = 10, pad = 0)
        self.grid_rowconfigure(4, weight = 0, minsize = 10, pad = 0)
        self.grid_rowconfigure(6, weight = 0, minsize = 10, pad = 0)
        self.grid_rowconfigure(8, weight = 0, minsize = 10, pad = 0)
        self.grid_columnconfigure(0, weight = 0, minsize = 20, pad = 0)
        self.grid_columnconfigure(2, weight = 0, minsize = 20, pad = 0)
        self.createWidgets()
        self.refresh_tags()
        self.refresh_posts()

    def createWidgets(self):
        print tkFont.families()
        font = tkFont.Font(family = "fixed", size = 14, weight="normal")
        self.search = Entry(self, bg = "#FFFFFF")
        self.search.bind("<KeyPress-Return>", self.on_search_changed)
        self.search.grid(row = 1, column = 1, sticky=W)
        #tag list frame
        self.tagList = ZListBox(self)
        self.tagList.grid(row = 3, column = 1, sticky=W)
        self.tagList.on_row_click(self.on_tag_clicked)
        #post list frame
        self.postList = ZListBox(self, width = 60, height = 30)
        self.postList.grid(row = 5, column = 1, sticky=W)
        self.postList.on_row_click(self.tagList.clear_selection)
        self.postList.on_row_dbl_click(self.on_post_dbl_clicked)
        #quit button
        self.quitButton = Button(self, text="Quit", command=self.quit)
        self.quitButton.grid(row = 7, column = 1)
    
    def refresh_tags(self, tag=""):
        tags = self.cache.findTags(tag)
        print "tags found : ", len(tags)
        self.tagList.set_data(tags, lambda item: item[0])
        
    def refresh_posts(self, tag="", exact=False):
        print "refreshing posts list for tag : ", tag
        self.posts = self.cache.find_posts_by_tag(tag, exact)
        print "posts found : ", len(self.posts)
        self.postList.set_data(self.posts, lambda item: item[0])       
    
    def on_search_changed(self, event):
        print "char : ", event.char
        print "search : ", self.search.get()
        self.refresh_tags(self.search.get())
        self.refresh_posts(self.search.get())
        
    def on_tag_clicked(self, event):
        print event.widget.curselection()
        print self.tagList._list.curselection()
        tag = self.tagList.get_current_row()
        self.refresh_posts(tag)
        
    def on_post_dbl_clicked(self, event):
        index = self.postList.get_current_index()
        print "selected index : ", index
        post = self.posts[index]
        print "selected post : ", post
        print "goto url : ", post[1]
        webbrowser.open_new_tab(post[1])

class ZListBox(Frame):
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master)
        yScroll = Scrollbar(self, orient=VERTICAL)
        yScroll.grid(row=0, column=1, sticky=N+S)
        self._list = Listbox(self, kw, bg = "#FFFFFF", yscrollcommand=yScroll.set)
        yScroll["command"]  =  self._list.yview
        self._list.grid(row = 0, column = 0, sticky=W)
        print self._list
        
    def set_data(self, data, func):
        self.clear_data()
        for item in data:
            self._list.insert(END, func(item))
            
    def get_current_index(self):
        return int(self._list.curselection()[0])
    
    def get_current_row(self):
        return self._list.get(self.get_current_index())
            
    def clear_data(self):
        self._list.delete(0, self._list.size())
        
    def clear_selection(self, event=None):
        print self._list.curselection()
        self._list.selection_clear(0, END)
        
    def on_row_dbl_click(self, func):
        self._list.bind("<Double-Button-1>", func)
        
    def on_row_click(self, func):
        self._list.bind("<<ListboxSelect>>", func)      

def main():
    root = Tk()
#    root.tk.call('package', 'require', 'tile')
#    root.tk.call('namespace', 'import', '-force', 'ttk::*')
#    root.tk.call('tile::setTheme', 'clam')
    app = DiliciousApplication(root)
    root.mainloop()      
    
if __name__ == '__main__':
    main()
