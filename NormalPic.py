from tkinter import *
import tkinter.font as tkFont
import menu_items
from customtkinter import *
from CameraViewer import MyVideoCapture
from PIL import Image, ImageTk
import cv2 as cv
import time
from cameraDemo import *
import math
from ConfirmPage import *

class PicPreview(CTkFrame):
    def __init__(self, master, source: int=0, filters: bool=False, images=None):
        global swap; swap = False
        self.images = images            

        super().__init__()
        self.cam = MyVideoCapture(source=source)
        self.preview = Canvas(master=self, width=self.cam.width, height=self.cam.height)
        self.master = master
        self.backButton = CTkButton(master=self, text="Back to Main menu",
                                    command=lambda: master.switch_menu(menu_items.MainMenu))
        self.inverseButton = CTkButton(master=self, text="Greyscale/Color",
                                    command=self.cam.swapColor, state=DISABLED if filters else NORMAL)
        self.picButton = CTkButton(master=self, text="TAKE A PIC",
                                    command=self.snap)
        self.filters = filters
        self.textID = None
        self.font = tkFont.Font(family='Helvetica',
                                size=180, weight='bold')
        #self.swap = lambda img: master.switch_menu(FinalImage, image=img)

        self.time = 0
        self.framerate = 20

        self.columnconfigure((0,1,2), weight=1)
        self.rowconfigure((0,1,2), weight=1)

        self.preview.grid(column=0, row=0, padx=10, pady=10, sticky=(N,W), columnspan=2, rowspan=2)
        self.backButton.grid(column=0, row=2,padx=10, pady=10, sticky=NSEW)
        self.inverseButton.grid(column=1, row=2,padx=10, pady=10, sticky=NSEW)
        self.picButton.grid(column=2, row=0, padx=10, pady=10, sticky=NSEW, rowspan=3)

        self.update()

    def snap(self):
        self.time=3

    def get_frame(self):
        if self.filters == True:
            ret, frame = take_pic_2(self.cam.vid)

        else:
            ret, frame = self.cam.get_frame()

        if ret:
            global swap; swap = True
            if self.images is None:
                self.images = []
            self.master.switch_menu(FinalImage, images=self.images.append(frame) if self.images is not None else frame, col=self.cam.color, filters=self.filters)

    def update(self):
        if swap:
            return

        frame = self.cam.get_frame()
        if ret:
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.preview.create_image(0, 0, image = self.photo, anchor = NW)

        if self.time is not None:
            if self.time > 0:
                self.time -= (1000//self.framerate)/1000
                if self.textID is not None:
                    self.preview.delete(self.textID)
            
                self.textID = self.preview.create_text(self.cam.width//2, self.cam.height//2, 
                                                        text=f'{math.ceil(self.time)}', font=self.font)

            elif self.time < 0:
                self.get_frame()
                self.time = None

        self.master.after(1000//self.framerate, self.update)

    def timer(self):
        self.time -= 1

        if self.time < 1:
            self.get_frame()
            self.textID = None
            return

        if self.textID is not None:
            self.preview.delete(self.textID)
        
        self.textID = self.preview.create_text(self.cam.width//2, self.cam.height//2, 
                                                text=f'{self.time}', font=self.font)
        self.after(1000, self.timer)