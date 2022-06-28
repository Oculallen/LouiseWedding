from tkinter import *
from customtkinter import *

class MainMenu(CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.normalPic = CTkButton(self, text="Normal Picture")
        self.filterPic = CTkButton(self, text="Filter Picture")

        self.normalPic.grid(column=0, row=0, pady=30, padx=30)
        self.filterPic.grid(column=1, row=0, pady=30, padx=30)