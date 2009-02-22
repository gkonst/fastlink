'''
Created on Feb 22, 2009

@author: kostya
'''
from Tkinter import *

class ZDialog(Toplevel):

    def __init__(self, parent, title = None):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
        self.parent = parent
        self.result = None
        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)
        self.buttonbox()
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))
        self.initial_focus.focus_set()
        self.wait_window(self)

    #
    # construction hooks
    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons        
        box = Frame(self)
        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

    #
    # standard button semantics
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks
    def validate(self):
        return 1 # override

    def apply(self):
        pass # override
    
class ZEntry(Frame):
    def __init__(self, master=None, label="", value="", **kw):
        Frame.__init__(self, master)
        if label:
            label = Label(self, text=label)
            label.grid(row = 0, column = 0)
        self._value = StringVar(value=value)
        entry = Entry(self, bg = "#FFFFFF", textvariable=self._value, **kw)
        entry.grid(row = 0, column = 1)
        
    def value(self, value=None):
        if value:
            self._value.set(value)
        else:
            return self._value.get()
        
class ZPasswordEntry(ZEntry):
    def __init__(self, master=None, label="", value="", **kw):
        ZEntry.__init__(self, master, label=label, value=value, show="*", **kw)
        
class ZListBox(Frame):
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master)
        yScroll = Scrollbar(self, orient=VERTICAL)
        yScroll.grid(row=0, column=1, sticky=N+S)
        self._list = Listbox(self, kw, bg = "#FFFFFF", yscrollcommand=yScroll.set)
        yScroll["command"]  =  self._list.yview
        self._list.grid(row = 0, column = 0, sticky=W)
        
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
        self._list.selection_clear(0, END)
        
    def on_row_dbl_click(self, func):
        self._list.bind("<Double-Button-1>", func)
        
    def on_row_click(self, func):
        self._list.bind("<<ListboxSelect>>", func) 
