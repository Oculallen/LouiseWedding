import cv2 as cv

class MyVideoCapture:
    def __init__(self, source: int=0):
        self.source = source
        self.vid = cv.VideoCapture(source)
        ret, frame = self.vid.read()
        res_frame = self.resize(frame)
        if not self.vid.isOpened():
            raise ValueError("Unable to open Video Source", source)

        self.width = res_frame.shape[1]
        self.height = res_frame.shape[0]
        self.color = cv.COLOR_BGR2RGB
    
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv.cvtColor(self.resize(frame), self.color))
            else:
                return (ret, None)
        else:
            return (False, None)

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