from tkinter import *
import tkinter.font as tkFont
import menu_items
from customtkinter import *
from CameraViewer import MyVideoCapture
from PIL import Image, ImageTk
import cv2 as cv
import time
from cameraDemo import *

class PicPreview(CTkFrame):
    def __init__(self, master, source: int=0, filters: bool=False):
        super().__init__(master)
        self.cam = MyVideoCapture(source=source)
        self.preview = Canvas(master=self, width=self.cam.width, height=self.cam.height)
        self.master = master
        self.backButton = CTkButton(master=self, text="Back to Main menu",
                                    command=lambda: master.switch_menu(menu_items.MainMenu))
        self.inverseButton = CTkButton(master=self, text="Greyscale/Color",
                                    command=self.cam.swapColor)
        self.picButton = CTkButton(master=self, text="TAKE A PIC",
                                    command=self.snap)
        self.filters = filters
        self.textID = None
        self.font = tkFont.Font(family='Helvetica',
                                size=60, weight='bold')

        self.columnconfigure((0,1,2), weight=1)
        self.rowconfigure((0,1,2), weight=1)

        self.preview.grid(column=0, row=0, padx=10, pady=10, sticky=(N,W), columnspan=2, rowspan=2)
        self.backButton.grid(column=0, row=2,padx=10, pady=10, sticky=NSEW)
        self.inverseButton.grid(column=1, row=2,padx=10, pady=10, sticky=NSEW)
        self.picButton.grid(column=2, row=0, padx=10, pady=10, sticky=NSEW, rowspan=3)

        self.update()

    def snap(self):
        self.timer(3, self.get_frame)

    def get_frame(self):
        if self.filters == True:
            take_pic_2(self.cam.vid)

        else:
            ret, frame = self.cam.get_frame()

            if ret:
                cv.imwrite("picture-" + time.strftime("%d-%m-%Y-%H-%M") + ".jpg", 
                cv.cvtColor(frame, self.cam.color) if self.cam.color == cv.COLOR_BGR2RGB else frame)

    def update(self):
        ret, frame = self.cam.get_frame()
        if ret:
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.preview.create_image(0, 0, image = self.photo, anchor = NW)

        self.master.after(40, self.update)

    def timer(self, time: int, func):
        if time < 1:
            func()
            self.textID = None
            return

        if self.textID is not None:
            self.preview.delete(self.textID)
        
        self.textID = self.preview.create_text(0, 0, text=f'{time}', font=self.font)
        self.master.after(1000, self.timer(time-1, func))