from tkinter import *
from customtkinter import *
from menu_items import *
from NormalPic import *

class App(CTk):
    #Cool shit happens here
    #Nice
    def __init__(self):
        super().__init__()
        self.attributes("-fullscreen", True)
        self.protocol("WM_DELETE_WINDOW", self.end)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.menu = None

        self.switch_menu(MainMenu)

    def switch_menu(self, menu_class, *args, **kwargs):
        new_menu = menu_class(self, *args, **kwargs)
        if self.menu is not None:
            self.menu.destroy()
        self.menu = new_menu

        self.menu.grid(column=0, row=0, sticky=NSEW)

    def start(self):
        self.mainloop()

    def end(self):
        self.destroy()

app = App()
app.start()