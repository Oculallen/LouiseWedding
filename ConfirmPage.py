from tkinter import *
import tkinter.font as tkFont
from customtkinter import *
from PIL import Image, ImageTk
import cv2 as cv

class FinalImage(CTkFrame):
    def __init__(self, master, image=None, col=None):
        super().__init__()
        print(image.shape)
        self.preview = CTkCanvas(master=self, width=image.shape[1], height=image.shape[0])
        self.retryButton = CTkButton(self, text="Retry")
        self.takeAnother = CTkButton(self, text="Take Another")
        self.savePics = CTkButton(self, text="Save All Pics")

        self.columnconfigure((0,1,2), weight=1)
        self.rowconfigure((0,1), weight=1)

        self.preview.grid(column=0, row=0, columnspan=3)
        self.retryButton.grid(column=0, row=1)
        self.takeAnother.grid(column=1, row=1)
        self.savePics.grid(column=2, row=1)

        self.pic = ImageTk.PhotoImage(image = Image.fromarray(image))
        self.img = cv.cvtColor(image, col) if col == cv.COLOR_BGR2RGB else image
        self.init_canvas()
    
    def init_canvas(self):
        self.preview.create_image(0, 0, image = self.pic, anchor = NW)