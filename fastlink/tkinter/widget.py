# -*- coding: utf-8 -*-
'''
Contains custom **Tkinter** widgets.

.. moduleauthor:: Konstantin_Grigoriev <Konstantin.V.Grigoriev@gmail.com>
'''
import os
from multiprocessing import Queue
from Tkinter import *
import tkMessageBox

class ZDialog(Toplevel):

    def __init__(self, parent, title=None):
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
        self.update()
        self.after_idle(center_on_screen, self)
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
            label.grid(row=0, column=0)
        self._value = StringVar(value=value)
        self._entry = Entry(self, background="#FFFFFF", textvariable=self._value, **kw)
        self._entry.grid(row=0, column=1)
    
    def __getitem__(self, key):
        return self._entry.__getitem__(key)
    
    def __setitem__(self, key, value):
        self._entry.__setitem__(key, value)
        
    def value(self, value=None):
        if value:
            self._value.set(value)
        else:
            return self._value.get()
        
    def add_listener(self, action, listener):
        self._entry.bind(action, listener)
        
    def focus(self):
        self._entry.focus_set()
        
class ZPasswordEntry(ZEntry):
    def __init__(self, master=None, label="", value="", **kw):
        ZEntry.__init__(self, master, label=label, value=value, show="*", **kw)
        
class ZListBox(Frame):
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master)
        yScroll = Scrollbar(self, orient=VERTICAL)
        yScroll.grid(row=0, column=1, sticky=N + S)
        self._list = Listbox(self, background="#FFFFFF", yscrollcommand=yScroll.set, **kw)
        yScroll["command"] = self._list.yview
        self._list.grid(row=0, column=0, sticky=W)
        
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

class ZSplashScreen(Toplevel):
    '''
    A **Tkinter** splash screen (uses a GIF image file, does not need PIL).
    '''
    def __init__(self, master, image_file=None, timeout=None):
        """
        Create a splash screen from a specified image file
        keep splash screen up for timeout milliseconds.
        """
        Toplevel.__init__(self, master, relief='raised', borderwidth=1)

        # don't show main window
#        self.main.withdraw()
#        self.overrideredirect(1)
        
        # emulate modal      
        self.grab_set()
        self.focus_set()
        
        self.i = 0  
        if image_file and os.path.exists(image_file % self.i):
            # Use image if exist
            # use Tkinter's PhotoImage for .gif files
            image = PhotoImage(file=image_file % self.i)
            self.canvas = Canvas(self, height=image.height(), width=image.width(), relief='raised', borderwidth=0)
            self.canvas.create_image(0, 0, anchor='nw', image=image)
            self.canvas.pack()
            self.image_file = image_file
        else:
            self.image_file = None
            # Use text instead of image
            Label(self, text='Working...').pack()   
        center_on_screen(self)     
        self.queue = Queue()
        if timeout:
            self.after(timeout, self.destroy_splash)

    def start_splash(self):
        self._animate()
        
    def _animate(self):
        if self.image_file:
            if not os.path.exists(self.image_file % self.i):
                self.i = 0
            image = PhotoImage(file=self.image_file % self.i)
            self.canvas.create_image(0, 0, anchor='nw', image=image)
            self.canvas.update()  
            self.i = self.i + 1
        if self.queue.empty():
            self.after_idle(self._animate)
        elif 'ERROR' in self.queue.get():
#            tkMessageBox.showerror('Error during saving', self.queue.get())
            self.destroy_splash()            
        else:
            self.destroy_splash()
            self.quit()               

    def destroy_splash(self):
        # bring back main window and destroy splash screen
        self.master.update()
#        self.main.deiconify()
        self.withdraw()
        self.destroy()
        
    def stop_splash(self):
        self.queue.put('STOP')
       
def center_on_screen(widget, width=None, height=None):
    if not width or not height:
        widget.update()
        width, height = widget.winfo_width(), widget.winfo_height()
    widget.update_idletasks()

    xmax = widget.winfo_screenwidth()
    ymax = widget.winfo_screenheight()

    x0 = xmax / 2 - width / 2
    y0 = ymax / 2 - height / 2
    widget.winfo_toplevel().geometry("%dx%d+%d+%d" % (width, height, x0, y0))    
