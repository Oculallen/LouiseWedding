import cv2 as cv
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

class MyVideoCapture:
    def __init__(self, source: int=0):
        self.source = source
        #self.vid = PiCamera(resolution=(1920,1080))
        self.vid = cv.VideoCapture(source)
        #self.rawcap = PiRGBArray(self.vid, size=(1920,1080))
        #self.stream = self.camera.capture_continuous(self.rawCapture,
        #    format="bgr")
        ret, frame = self.vid.read()
        res_frame = self.resize(frame)
        if not self.vid.isOpened():
            raise ValueError("Unable to open Video Source", source)

        # time.sleep(0.1)

        # self.vid.capture(self.rawcap, format="bgr")
        # image = self.rawcap.array

        self.width = image.shape[1]
        self.height = image.shape[0]
        self.color = cv.COLOR_BGR2RGB
    
    # def __del__(self):
    #     if self.vid.isOpened():
    #         self.vid.release()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv.cvtColor(self.resize(frame), self.color))
            else:
                return (ret, None)
        else:
            return (False, None)
        # f = self.stream.__next__()
        # img = f.array
        # self.rawcap.truncate(0)
        # self.rawcap.seek(0)

        #return True, cv.cvtColor(self.resize(img), self.color)

    def resize(self, frame, width: int=1250):
        hFactor = width/frame.shape[1]
        nheight = int(frame.shape[0] * hFactor)

        nframe = cv.resize(frame, [width, nheight])
        return nframe

    def swapColor(self):
        if self.color == cv.COLOR_BGR2RGB:
            self.color = cv.COLOR_BGR2GRAY
        else:
            self.color = cv.COLOR_BGR2RGB