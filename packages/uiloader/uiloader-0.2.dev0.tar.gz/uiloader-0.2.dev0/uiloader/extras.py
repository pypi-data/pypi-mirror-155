
from tkinter import (Tk as tk, Label as label, Button as button, Entry as entry, Frame as frame, Listbox as listbox, Radiobutton as radiobutton,
Checkbutton as checkbutton, Scale as scale, OptionMenu as optionmenu, Scrollbar as scrollbar, Text as textarea, Canvas as canvas, Toplevel, Widget)
from tkinter.ttk import (Combobox as combobox)
from threading import Thread
from PIL import ImageTk,Image as IMAGE 
class Tk(tk):
    def __init__(self, *args, **kwargs):
        tk.__init__(self, *args, **kwargs)
        self.events = {}

    def Bind(self, key, func):
        if key not in self.events:
            self.events.update({key:[]})
            self.events[key].append(func)
        else:
            self.events[key].append(func)
        self.bind(key, lambda event: [i(event) for i in self.events[key]])
        
class Label(label):
    def __init__(self, master, *args, **kwargs):
        label.__init__(self, master, *args, **kwargs)
        self.opts = {"default_fg":self["fg"], "default_bg":self["bg"], "hoverfg":"", "unhoverfg":self["fg"], "hoverbg":"", "unhoverbg":self["bg"]}
        self.events = {}

    def Bind(self, key, func):
        if key not in self.events:
            self.events.update({key:[]})
            self.events[key].append(func)
        else:
            self.events[key].append(func)
        self.bind(key, lambda event: [i(event) for i in self.events[key]])

    def Place(self, *args, **kwargs):
        self.grid_info = args, kwargs

    def Show(self):
        self.grid(self.grid_info)

    def Hide(self):
        self.grid_forget()

class Button(button):
    def __init__(self, master, *args, **kwargs):
        button.__init__(self, master, *args, **kwargs)
        self.clicked = False
        self.events = {}

    def Bind(self, key, func):
        if key not in self.events:
            self.events.update({key:[]})
            self.events[key].append(func)
        else:
            self.events[key].append(func)
        self.bind(key, lambda event: [i(event) for i in self.events[key]])

    def CreatePopupMsg(self, msg=None):
        self.Popup = PopupMsg(self, msg)
        self.Popup.withdraw()
        self.Bind("<Enter>", self.ShowPopupMsg)
        self.Bind("<Leave>", self.HidePopupMsg)

    def ShowPopupMsg(self, event):
        self.Popup.UpdatePos()
        self.Popup.deiconify()

    def HidePopupMsg(self, event):
        self.Popup.withdraw()

    def DeletePopupMsg(self, event):
        self.Popup.destroy()
        self.unbind("<Enter>", self.ShowPopupMsg)
        self.unbind("<Leave>", self.HidePopupMsg)

    def Place(self, *args, **kwargs):
        self.grid_info = args, kwargs

    def Show(self):
        self.grid(self.grid_info)

    def Hide(self):
        self.grid_forget()
    
class Entry(entry):
    def __init__(self, master, *args, **kwargs):
        entry.__init__(self, master, *args, **kwargs)
        self.opts = ( {"default_fg":"", "default_bg":"", "hoverfg":"", "unhoverfg":"", "hoverbg":"", "unhoverbg":""})
        self.opts["default_fg"] = self["foreground"]
        self.opts["default_bg"] = self["background"]
        self.events = {}

    def Bind(self, key, func):
        if key not in self.events:
            self.events.update({key:[]})
            self.events[key].append(func)
        else:
            self.events[key].append(func)
        self.bind(key, lambda event: [i(event) for i in self.events[key]])

    def HoverBind(self, fg=None, bg=None):
        self.Bind("<Enter>", lambda event: self.OnHover(event, fg, bg))

    def UnHoverBind(self, fg=None, bg=None):
        self.Bind("<Leave>", lambda event: self.UnHover(event, fg, bg))

    def OnHover(self, event, fg=None, bg=None):
        widget = event.widget
        widget["fg"] = fg if fg != None else None
        widget["bg"] = bg if bg != None else None
    
    def UnHover(self, event, fg=None, bg=None):
        widget = event.widget
        if fg == None:
            widget["fg"] = self.opts["default_fg"]
        else:
            widget["fg"] = fg
        if bg == None:
            widget["bg"] = self.opts["default_bg"]
        else:
            widget["bg"] = bg

    def __getitem__(self, key):
        if key not in self.config():
            return self.opts[key]
        else:
            return self.config()[key][4]
        
        
    def Place(self, *args, **kwargs):
        self.grid_info = args, kwargs

    def Show(self):
        self.grid(self.grid_info)

    def Hide(self):
        self.grid_forget()

class Frame(frame):
    def __init__(self, master, *args, **kwargs):
        frame.__init__(self, master, *args, **kwargs)
        self.clicked = False
        self.events = {}

    def Bind(self, key, func):
        if key not in self.events:
            self.events.update({key:[]})
            self.events[key].append(func)
        else:
            self.events[key].append(func)
        self.bind(key, lambda event: [i(event) for i in self.events[key]])

    def Place(self, *args, **kwargs):
        self.grid_info = args, kwargs

    def Show(self):
        self.grid(self.grid_info)

    def Hide(self):
        self.grid_forget()

class Listbox(listbox):
    def __init__(self, master, *args, **kwargs):
        listbox.__init__(self, master, *args, **kwargs)
        self.events = {}

    def Bind(self, key, func):
        if key not in self.events:
            self.events.update({key:[]})
            self.events[key].append(func)
        else:
            self.events[key].append(func)
        self.bind(key, lambda event: [i(event) for i in self.events[key]])

    def Place(self, *args, **kwargs):
        self.grid_info = args, kwargs

    def Show(self):
        self.grid(self.grid_info)

    def Hide(self):
        self.grid_forget()

class Radiobutton(radiobutton):
    def __init__(self, master, *args, **kwargs):
        radiobutton.__init__(self, master, *args, **kwargs)
        self.events = {}

    def Bind(self, key, func):
        if key not in self.events:
            self.events.update({key:[]})
            self.events[key].append(func)
        else:
            self.events[key].append(func)
        self.bind(key, lambda event: [i(event) for i in self.events[key]])

    def Place(self, *args, **kwargs):
        self.grid_info = args, kwargs

    def Show(self):
        self.grid(self.grid_info)

    def Hide(self):
        self.grid_forget()
    
class Checkbutton(checkbutton):
    def __init__(self, master, *args, **kwargs):
        checkbutton.__init__(self, master, *args, **kwargs)
        self.events = {}

    def Bind(self, key, func):
        if key not in self.events:
            self.events.update({key:[]})
            self.events[key].append(func)
        else:
            self.events[key].append(func)
        self.bind(key, lambda event: [i(event) for i in self.events[key]])

    def Place(self, *args, **kwargs):
        self.grid_info = args, kwargs

    def Show(self):
        self.grid(self.grid_info)

    def Hide(self):
        self.grid_forget()

class Scale(scale):
    def __init__(self, master, *args, **kwargs):
        scale.__init__(self, master, *args, **kwargs)
        self.events = {}

    def Bind(self, key, func):
        if key not in self.events:
            self.events.update({key:[]})
            self.events[key].append(func)
        else:
            self.events[key].append(func)
        self.bind(key, lambda event: [i(event) for i in self.events[key]])

    def Place(self, *args, **kwargs):
        self.grid_info = args, kwargs

    def Show(self):
        self.grid(self.grid_info)

    def Hide(self):
        self.grid_forget()
        
class Textarea(textarea):
    def __init__(self, master, *args, **kwargs):
        textarea.__init__(self, master, *args, **kwargs)
        self.events = {}

    def Bind(self, key, func):
        if key not in self.events:
            self.events.update({key:[]})
            self.events[key].append(func)
        else:
            self.events[key].append(func)
        self.bind(key, lambda event: [i(event) for i in self.events[key]])

    def Place(self, *args, **kwargs):
        self.grid_info = args, kwargs

    def Show(self):
        self.grid(self.grid_info)

    def Hide(self):
        self.grid_forget()

class OptionMenu(optionmenu):
    def __init__(self, master, *args, **kwargs):
        optionmenu.__init__(self, master, *args, **kwargs)
        self.events = {}

    def Bind(self, key, func):
        if key not in self.events:
            self.events.update({key:[]})
            self.events[key].append(func)
        else:
            self.events[key].append(func)
        self.bind(key, lambda event: [i(event) for i in self.events[key]])

    def Place(self, *args, **kwargs):
        self.grid_info = args, kwargs

    def Show(self):
        self.grid(self.grid_info)

    def Hide(self):
        self.grid_forget()

class Scrollbar(scrollbar):
    def __init__(self, master, *args, **kwargs):
        scrollbar.__init__(self, master, *args, **kwargs)
        self.events = {}

    def Bind(self, key, func):
        if key not in self.events:
            self.events.update({key:[]})
            self.events[key].append(func)
        else:
            self.events[key].append(func)
        self.bind(key, lambda event: [i(event) for i in self.events[key]])

    def Place(self, *args, **kwargs):
        self.grid_info = args, kwargs

    def Show(self):
        self.grid(self.grid_info)

    def Hide(self):
        self.grid_forget()

class Combobox(combobox):
    def __init__(self, master, *args, **kwargs):
        combobox.__init__(self, master, *args, **kwargs)
        self.events = {}

    def Bind(self, key, func):
        if key not in self.events:
            self.events.update({key:[]})
            self.events[key].append(func)
        else:
            self.events[key].append(func)
        self.bind(key, lambda event: [i(event) for i in self.events[key]])

    def Place(self, *args, **kwargs):
        self.grid_info = args, kwargs

    def Show(self):
        self.grid(self.grid_info)

    def Hide(self):
        self.grid_forget()

class PopupMsg(Toplevel):
    def __init__(self, master, msg, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)
        self.text = msg
        self.master = master
        self.wm_overrideredirect(True)
        label = Label(self, text=self.text, justify='left',
                       background='yellow', relief='solid', borderwidth=1,
                       font=("times", "14", "normal"))
        label.pack(ipadx=1)
        self.UpdatePos()

    def UpdatePos(self):
        x = y = 0
        x, y, cx, cy = self.master.bbox("insert")
        x += self.master.winfo_rootx() + 25
        y += self.master.winfo_rooty() + 30
        self.wm_geometry("+%d+%d" % (x, y))

class Canvas(canvas):
    def __init__(self, master, *args, **kwargs):
        canvas.__init__(self, master, *args, **kwargs)
        self.events = {}

    def Bind(self, key, func):
        if key not in self.events:
            self.events.update({key:[]})
            self.events[key].append(func)
        else:
            self.events[key].append(func)
        self.bind(key, lambda event: [i(event) for i in self.events[key]])

    def Place(self, *args, **kwargs):
        self.grid_info = args, kwargs

    def Show(self):
        self.grid(self.grid_info)

    def Hide(self):
        self.grid_forget()
        
class Image(label):
    def __init__(self, master, file, *args, **kwargs):
        label.__init__(self, master, *args, **kwargs)
        self.file = file
        self.master = master
        self.events = {}
        self.LoadImage()

    def Bind(self, key, func):
        if key not in self.events:
            self.events.update({key:[]})
            self.events[key].append(func)
        else:
            self.events[key].append(func)
        self.bind(key, lambda event: [i(event) for i in self.events[key]])

    def Place(self, *args, **kwargs):
        self.grid_info = args, kwargs

    def Show(self):
        self.grid(self.grid_info)

    def Hide(self):
        self.grid_forget()
        
    def LoadImage(self):
        file = IMAGE.open(self.file)
        img = ImageTk.PhotoImage(file)
        self.configure(image=img)
        self.image = img
        




