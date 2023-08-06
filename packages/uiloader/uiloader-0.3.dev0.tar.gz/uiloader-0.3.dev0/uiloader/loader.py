from uiloader.widgets import *
from uiloader.extras import *
from tkinter import TclError
gui = {}

class LoadScript(Tk):
    def __init__(self, name, master=None):
        if master == None:
            script = ""
            with open("{0}".format(name)) as f:
                script = f.read()
            window = eval(script)
            Tk.__init__(self)
            gui.update({window["name"]:self})
            gui[window["name"]].title(window["name"])
            self.LoadChildren(self, window)
        else:
            window = {"children":[]}
            with open("{0}".format(name)) as f:
                script = f.read()
            window.update({"children":[eval(script)]})
            print(master, window)
            #gui.update({window["name"]:self})
            self.LoadChildren(master, window)

    def LoadChildren(self, parent, window):
        search = self.SearchAttr
        if "children" in window:
            for obj in window["children"]:
                if not search(obj, "name"):
                    return self.RaiseError("name attribute not found for obj {0}".format(obj)) 
                if not search(obj, "type"):
                    return self.RaiseError("type attribute not found for obj {0}".format(obj)) 
                if obj["type"] == "frame":
                    gui.update({obj["name"]: self.GetWidget(Frame, parent, obj)})
                    self.GetWidget(gui[obj["name"]].place, None, obj)
                    if search(obj, "x") != None and search(obj, "y") != None:
                        self.GetWidget(gui[obj["name"]].place, None, obj)
                    elif search(obj, "row") != None and search(obj, "column") != None: 
                        self.GetWidget(gui[obj["name"]].grid, None, obj)
                    else:
                        self.GetWidget(gui[obj["name"]].grid, None, obj)
                    self.LoadChildren(gui[obj["name"]], obj)
                else:
                    gui.update({obj["name"]: self.GetWidget(widgets[obj["type"].title()]["obj"], parent, obj)})
                    if search(obj, "x") != None and search(obj, "y") != None:
                        self.GetWidget(gui[obj["name"]].place, None, obj)
                    elif search(obj, "row") != None and search(obj, "column") != None: 
                        self.GetWidget(gui[obj["name"]].grid, None, obj)
                    else:
                        self.GetWidget(gui[obj["name"]].grid, None, obj)


    def RaiseError(self, err):
        print(err)

    def SearchAttr(self, obj, attr):
        if obj:
            if attr in obj:
                attr = obj[attr]
            else:
                attr = None
            return attr
        return None

    def GetWidget(self, widget, parent, obj):
        saved = {}
        if obj:
            while True:
                try:
                    if parent:
                        the_widget = widget(parent, **self.GetArgs(obj))
                    else:
                        the_widget = widget(**self.GetArgs(obj))
                    for i in saved:
                        obj.update({i:saved[i]})
                    return the_widget
                except TclError as err:
                    missing = str(err).split('"')[1].replace("-", "")
                    if missing == "highlightbackground" or missing == "highlightcolor":
                        missing = "borderbg"
                    elif missing == "highlightthickness":
                        missing = "borderthick"
                    if missing == "column":
                        missing = "col"
                    saved.update({missing:obj[missing]})
                    del obj[missing]
        else:
            return None

    def GetArgs(self, obj):
        search = self.SearchAttr
        args = {}
        if obj:
            for key in obj:
                attr = key
                if key != "name":
                    if key == "borderbg":
                        attr = "highlightbackground"
                        args.update({"highlightcolor":search(obj, "borderbg")})
                    elif key == "borderthick":
                        attr = "highlightthickness"
                    elif key == "col":
                        attr = "column"
                    args.update({attr:search(obj, key)})

        return args

    def __getitem__(self, name):
        return gui[name]