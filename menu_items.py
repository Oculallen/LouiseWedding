from tkinter import *
from customtkinter import *
from NormalPic import PicPreview

class MainMenu(CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.normalPic = CTkButton(self, text="Normal Picture",
                            command=lambda: master.switch_menu(PicPreview, source=0, filters=False))
        self.filterPic = CTkButton(self, text="Filter Picture",
                            command=lambda: master.switch_menu(PicPreview, source=0, filters=True))

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.normalPic.grid(column=0, row=0, sticky=NSEW, padx=10, pady=10)
        self.filterPic.grid(column=1, row=0, sticky=NSEW, padx=10, pady=10)

    def _load_preview(self, filters: bool=False):
        pass