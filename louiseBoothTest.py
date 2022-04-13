import dlib
import cv2
import numpy as np
from scipy import ndimage
 
glasses = cv2.imread("Images/bride.png", -1)
video_capture = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
 
#Resize an image to a certain width
def resize(img, width):
    r = float(width) / img.shape[1]
    dim = (width, int(img.shape[0] * r))
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return img
 
#Combine an image that has a transparency alpha channel
def blend_transparent(face_img, sunglasses_img):
 
    overlay_img = sunglasses_img[:,:,:3]
    overlay_mask = sunglasses_img[:,:,3:]
     
    background_mask = 255 - overlay_mask
 
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)
 
    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))
 
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))
 
#Find the angle between two points
def angle_between(point_1, point_2):
    angle_1 = np.arctan2(*point_1[::-1])
    angle_2 = np.arctan2(*point_2[::-1])
    return np.rad2deg((angle_1 - angle_2) % (2 * np.pi))
 
def take_a_pic():
    
    ret, img = video_capture.read()
    if not ret:
        print("failed to grab frame")
    img = resize(img, 700)
    img_copy = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
    try:
        # detect faces
        dets = detector(gray, 1)
 
        #find face box bounding points
        coords = []
        for d in dets:
            print("found one!")
            x = d.left()
            y = d.top()
            w = d.right()
            h = d.bottom()
            coords.append({"x": x,"y":y,"w": w,"h": h})
        print(coords)
 
        for coord in coords:
            dlib_rect = dlib.rectangle(coord['x'], coord['y'], coord['w'], coord['h'])
    
            ##############   Find facial landmarks   ##############
            detected_landmarks = predictor(gray, dlib_rect).parts()
    
            landmarks = np.matrix([[p.x, p.y] for p in detected_landmarks])
    
            for idx, point in enumerate(landmarks):
                pos = (point[0, 0], point[0, 1])
                if idx == 0:
                    eye_left = pos
                elif idx == 16:
                    eye_right = pos
    
                try:
                    #cv2.line(img_copy, eye_left, eye_right, color=(0, 255, 255))
                    degree = np.rad2deg(np.arctan2(eye_left[0] - eye_right[0], eye_left[1] - eye_right[1]))
    
                except:
                    pass
    
            ##############   Resize and rotate glasses   ##############
    
            #Translate facial object based on input object.
    
            eye_center = (eye_left[1] + eye_right[1]) / 2
    
            #Sunglasses translation
            #glass_trans = int(.2 * (eye_center - y))
    
            #Funny tanslation
            #glass_trans = int(-.3 * (eye_center - y ))
    
            # Mask translation
            glass_trans = int(-.2 * (eye_center - coord['y']))
    
            # Snap filter translation
            #glass_trans = int(-1.3 * (eye_center - y))
    
            # resize glasses to width of face and blend images
            face_width = coord['w'] - coord['x']
    
            # resize_glasses
            glasses_resize = resize(glasses, face_width)
    
            # Rotate glasses based on angle between eyes
            yG, xG, cG = glasses_resize.shape
            glasses_resize_rotated = ndimage.rotate(glasses_resize, (degree+90))
            glass_rec_rotated = ndimage.rotate(img[coord['y'] + glass_trans:coord['y'] + yG + glass_trans, coord['x']:coord['w']], (degree+90))
    
    
            #blending with rotation
            h5, w5, s5 = glass_rec_rotated.shape
            rec_resize = img_copy[coord['y'] + glass_trans:coord['y'] + h5 + glass_trans, coord['x']:coord['x'] + w5]
            blend_glass3 = blend_transparent(rec_resize , glasses_resize_rotated)
            img_copy[coord['y'] + glass_trans:coord['y'] + h5 + glass_trans, coord['x']:coord['x']+w5 ] = blend_glass3
            img = img_copy
        cv2.imwrite("opencvTest.png", img_copy)
        print("Done")
    except BaseException as err:
        print(err)

#Start main program
if __name__ == "__main__":
    while True:
        while True:
            ret, img = video_capture.read()
            if ret == True:
                cv2.imshow("Preview", img)
                if cv2.waitKey(1) & 0xFF == ord('y'):
                    break
                 
        #cv2.destroyAllWindows()
        take_a_pic()