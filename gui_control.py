from tkinter import *
from customtkinter import *
from menu_items import *

class App(CTk):
    def __init__(self):
        super().__init__()
        self.attributes("-fullscreen", True)
        self.protocol("WM_DELETE_WINDOW", self.end)
        self.resizable(False, False)

        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)

        self.menu = MainMenu(self)
        self.menu.grid(column=0, row=0, sticky=(N,S))

    def start(self):
        self.mainloop()

    def end(self):
        self.destroy()

app = App()
app.start()