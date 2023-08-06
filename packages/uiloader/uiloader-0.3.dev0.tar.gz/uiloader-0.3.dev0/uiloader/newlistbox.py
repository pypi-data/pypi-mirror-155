from uiloader.extras import *
from tkinter import NSEW, CENTER, Canvas, HORIZONTAL, VERTICAL, EW, NS, ALL

class Newlistbox(Frame):
    def __init__(self, master, title="None", content={"Sample":{"subtitles":["sub1", "sub2"]}}, state="normal", clickable_count=None, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.state = state
        self.clickable_count = clickable_count
        self.Tree = {}
        for main in content:
            Title = main
        self.Title = Label(self, font=("Bahnschrift SemiBold", 15), text=Title)
        self.Title.Place(sticky=NSEW, padx=20)
        self.Title.Show()
        self.SubTitleGrid = SubTitleGrid(self)
        self.SubTitleGrid.Place(row=1, column=0, sticky=NSEW, padx=20)
        self.SubTitleGrid.Show()
        for title in enumerate(content[Title]["subtitles"]):
            subtitle = Entry(self.SubTitleGrid, font=("Bahnschrift SemiBold", 12), text=title[1], justify=CENTER, width=20, bg="SystemButtonFace", fg="black", cursor="arrow", relief="flat")
            subtitle.delete(0, "end")
            subtitle.insert(0, title[1])
            subtitle.Place(row=0, column=title[0], sticky=NSEW)
            subtitle.Show()
        self.ContentGrid = ContentGrid(self)
        self.ContentGrid.Place(row=2, column=0, sticky=NSEW, padx=20)
        self.ContentGrid.Show()
        self.GridCanvas = Canvas(self.ContentGrid, width=200)
        self.GridCanvas.grid(row=2, column=0)
        self.hsbar = Scrollbar(self, orient=HORIZONTAL, command=self.GridCanvas.xview)
        self.hsbar.grid(row=3, column=0, sticky=EW)
        self.GridCanvas.config(xscrollcommand=self.hsbar.set)
        #self.titlecanvas.config(xscrollcommand=self.hsbar.set)
        self.vsbar = Scrollbar(self, orient=VERTICAL, command=self.GridCanvas.yview)
        self.vsbar.grid(row=2, column=1, sticky=NS)
        self.GridCanvas.config(yscrollcommand=self.vsbar.set)
        self.conf = {}
        if "conf" in content[Title]:
            for main in enumerate(content[Title]["conf"]):
                for index in enumerate(content[Title]["conf"][main[1]]):
                    for name in content[Title]["conf"][main[1]][index[1]]:
                        conf = {"font":("Bahnschrift SemiBold", 12), "justify":"center", "width":20, "bg":"SystemButtonFace", "fg":"black", "cursor":"arrow", "relief":"flat"}
                        for sub in enumerate(content[Title]["conf"][main[1]][index[1]]):
                            conf.update(**content[Title]["conf"][main[1]][index[1]][name])
                            #content[Title]["content"][main[1]][index[1]].update({name:{"font":("Bahnschrift SemiBold", 12), "justify":"center", "width":20, "bg":"SystemButtonFace", "fg":"black", "cursor":"arrow", "relief":"flat"}})
                            content[Title]["conf"][main[1]][index[1]][name] = conf
                            if "type" in content[Title]["conf"][main[1]][index[1]][name]:
                                print(content[Title]["conf"][main[1]][index[1]][name]["type"])
                            if self.state == "readonly":
                                if not "type" in content[Title]["conf"][main[1]][index[1]][name]:
                                    content[Title]["conf"][main[1]][index[1]][name].update({"disabledforeground":"black", "disabledbackground":"SystemButtonFace"})
            self.Update(content, Title)
        if self.state == "readonly":
            for main in self.Tree:
                for sub in self.Tree[main]:
                    self.Tree[main][sub]["state"] = "readonly"

    def GetValueByNum(self, col, value):
        for sub in enumerate(self.conf[str(col)]):
            if int(value) == sub[0]:
                return sub

    def Update(self, content, Title):
        from uiloader.widgets import widgets
        self.container = Frame(self.ContentGrid)
        for main in enumerate(content[Title]["conf"]):
            self.Tree.update({main[0]:{}})
            Menu = MenuGrid(self.container)
            Menu.Place(row=main[0], column=0, sticky=NSEW)
            Menu.Show()
            Menu.Bind("<Enter>", self.hover)
            Menu.Bind("<Leave>", self.unhover)
            is_entry = True
            for index in enumerate(content[Title]["conf"][main[1]]):
                self.Tree[main[0]].update({index[1]:{}})
                for name in content[Title]["conf"][main[1]][index[1]]:
                    if "type" in content[Title]["conf"][main[1]][index[1]][name]:
                        is_entry = False
                        print(content[Title]["conf"][main[1]][index[1]][name])
                        obj = widgets[content[Title]["conf"][main[1]][index[1]][name]["type"]]["obj"]
                        del content[Title]["conf"][main[1]][index[1]][name]["type"]
                        self.Tree[main[0]][index[1]].update({name:obj(Menu, **content[Title]["conf"][main[1]][index[1]][name])})
                        self.Tree[main[0]][index[1]][name]["text"] = name
                    else:
                        self.Tree[main[0]][index[1]].update({name:Entry(Menu, **content[Title]["conf"][main[1]][index[1]][name])})
                        self.Tree[main[0]][index[1]][name].insert(0, name)

                    self.Tree[main[0]][index[1]][name].Place(row=0, column=index[1])
                    self.Tree[main[0]][index[1]][name].Show()
                    if is_entry:
                        self.Tree[main[0]][index[1]][name].Bind("<Double-Button-1>", self.onclick)
        self.GridCanvas.create_window((0,0), window=self.container, anchor="center")
        self.container.update_idletasks()
        self.bbox = self.GridCanvas.bbox(ALL)
        self.GridCanvas.configure(scrollregion=self.bbox,  width=self.container.winfo_children()[0].winfo_width() if self.container.winfo_children()[0].winfo_width()  > 0 else 100,
        height=200 if self.container.winfo_height() < 200 else 200)

    def hover(self, event):
        widget = event.widget
        for obj in widget.winfo_children():
            if not widget.clicked:
                if self.state != "readonly":
                    obj["bg"] = "light blue"
                else:
                    obj["state"] = "normal"
                    obj["disabledbackground"] = "light blue"
                    obj["disabledforeground"] = obj["default_fg"]
                    obj["state"] = "disabled"

    def unhover(self, event):
        widget = event.widget
        for obj in widget.winfo_children():
            if not widget.clicked:
                if self.state != "readonly":
                    obj["bg"] = obj["default_bg"]
                else:
                    obj["state"] = "normal"
                    obj["disabledbackground"] = obj["default_bg"]
                    obj["state"] = "disabled"
    
    def onclick(self, event):
        widget = event.widget
        for obj in self.container.winfo_children():
            if widget in obj.winfo_children():
                if not obj.clicked:
                    if self.isclickable():
                        obj.clicked = True
                        for sub in obj.winfo_children():
                            if self.state != "readonly":
                                sub["bg"] = "dodger blue"
                                sub["fg"] = "white"
                            else:
                                sub["state"] = "normal"
                                sub["disabledbackground"] = "dodger blue"
                                sub["disabledforeground"] = "white"
                                sub["state"] = "disabled"
                else:
                    obj.clicked = False
                    for sub in obj.winfo_children():
                        if self.state != "readonly":
                            sub["bg"] = sub["default_bg"]
                            sub["fg"] = sub["default_fg"]
                        else:
                            sub["state"] = "normal"
                            sub["disabledbackground"] = sub["default_bg"]
                            sub["disabledforeground"] = sub["default_fg"]
                            sub["state"] = "disabled"

    def isclickable(self):
        if self.clickable_count != None:
            count = 0
            for obj in self.container.winfo_children():
                if obj.clicked:
                    count += 1
            if count == self.clickable_count:
                return False
            else:
                return True
        else:
            return True

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

    def __getitem__(self, key):
        for main in self.Tree:
            #print(main)
            for sub in self.Tree[main]:
                if sub == key:
                    return self.Tree[main][key]
        #return self.Tree[key]

class SubTitleGrid(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

    def Place(self, *args, **kwargs):
        self.grid_info = args, kwargs

    def Show(self):
        self.grid(self.grid_info)

    def Hide(self):
        self.grid_forget()

class ContentGrid(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs) 

    def Place(self, *args, **kwargs):
        self.grid_info = args, kwargs

    def Show(self):
        self.grid(self.grid_info)

    def Hide(self):
        self.grid_forget()

class MenuGrid(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs) 

    def Place(self, *args, **kwargs):
        self.grid_info = args, kwargs

    def Show(self):
        self.grid(self.grid_info)

    def Hide(self):
        self.grid_forget()

if __name__=="__main__":
    root = Tk()
    listbox = Newlistbox(root, content={"Teszt":{"subtitles":["test1", "test2", "test3"], "content":{0:{"0":{"Yes":{"fg":"red"}}, "1":{"No":{}}, "2":{"No":{}}}}}} ,state=None, clickable_count=2)
    #listbox = Newlistbox(root, "teszt", ["test1", "test1"], [["TEST", "TEST"]], conf={"0":{0:{"fg":"blue"}, 1:{"fg":"red"}}} ,state=None, clickable_count=2)
    listbox.Place()
    listbox.Show()
    root.mainloop()