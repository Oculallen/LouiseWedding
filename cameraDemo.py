import mediapipe as mp
import cv2
import numpy as np
from scipy import ndimage
import math
from PIL import Image
import random
import os
import time

#MP SETUP5
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

drawing_spec = mp_drawing.DrawingSpec(thickness=  1, circle_radius=1)
video_capture = cv2.VideoCapture(0)

#FUNCTIONS
def load_filter():
    filter_name = random.choice(os.listdir("PrunedImages"))
    name, num = filter_name.split("_")
    print(f'{name}, {num}')
    if name == "glass":
        offset = 10
        face_resize = 1
    elif name == "mouth":
        offset = -70
        face_resize = 0.8
    elif name == "head":
        offset = 120
        face_resize = 1.2
    # elif name == "chin":
    #     offset = -90
    else:
        offset = 0
        face_resize = 1
    filter_img = cv2.imread(("PrunedImages/{0}".format(filter_name)), -1)
    return filter_img, offset, face_resize

def detect_faces(image, maxPeople=10, minConfidence=0.5):
    with mp_face_mesh.FaceMesh(max_num_faces=maxPeople,min_detection_confidence=minConfidence) as faces:

        image.flags.writeable = False
        results = faces.process(image)
        image.flags.writeable = True

        if results.multi_face_landmarks:
            return results
        else:
            return None

def get_center(point1, point2):
    x = int((point1[0] + point2[0])/2)
    y = int((point1[1] + point2[1])/2)

    return (x, y)

def get_left_eye(img, landmarks):
    """Gets x, y coordinates of the center of left eye

    Args:
        landmarks (FaceMesh landmark list): list of landmarks
    """
    shape = img.shape
    x = (int((landmarks[159].x)*shape[1]))
    y = (int((landmarks[159].y)*shape[0]))

    return (x,y)

def get_right_eye(img, landmarks):
    """Gets x, y coordinates of the center of right eye

    Args:
        landmarks (FaceMesh landmark list): list of landmarks
    """
    shape = img.shape
    x = (int((landmarks[386].x)*shape[1]))
    y = (int((landmarks[386].y)*shape[0]))

    return (x,y)

def get_face_width(img, landmarks):
    shape = img.shape
    x_dist = int((landmarks[454].x - landmarks[234].x)*shape[1])
    y_dist = int((landmarks[454].y - landmarks[234].y)*shape[0])
    return int(math.sqrt(math.pow(x_dist, 2) + math.pow(y_dist, 2)))

#Resize an image to a certain width
def resize(img, width):
    r = float(width) / img.shape[1]
    dim = (width, int(img.shape[0] * r))
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return img
 
#Combine an image that has a transparency alpha channel
def blend_transparent(face_img, sunglasses_img):
    print(face_img.shape)
    print(sunglasses_img.shape)
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

def get_box(img, landmarks):
    shape = img.shape
    top_left = int(landmarks[234].x * shape[1])
    bottom_left = int((landmarks[152].y*shape[0]))
    top_right = int(landmarks[454].x * shape[1])
    return top_left, bottom_left, top_right

def shift_center(eye_center, degree, shift):
    angle = (-1*degree)-90
    if angle < 0:
        shift_x = math.sin(angle) * shift
        shift_y = math.cos(angle) * shift
        shift_x = shift_x*-1
    else:
        shift_x = math.sin(angle) * shift
        shift_y = math.cos(angle) * shift
    return (int(eye_center[0]+shift_x), int(eye_center[1]+shift_y))

def take_pic_2(source, gray=False):
    ret, img = source.read()
    if not ret:
        print("failed to grab frame")
    img = resize(img, 700)
    img_copy = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    try:
        results = detect_faces(img, maxPeople=10, minConfidence=0.5)

        for face in results.multi_face_landmarks:
            try:
                print(len(face.landmark))
                eye_left = get_left_eye(gray, face.landmark)
                eye_right = get_right_eye(gray, face.landmark)
                face_width = get_face_width(gray, face.landmark)
                x, y, w = get_box(gray, face.landmark)
                degree = np.rad2deg(np.arctan2(eye_left[0] - eye_right[0], eye_left[1] - eye_right[1]))
                print(degree)
                eye_center = get_center(eye_right, eye_left)
                glasses, offset, face_resize = load_filter()
                #eye_center = shift_center(eye_center, degree, offset)
                eye_center = [eye_center[0], eye_center[1] - offset]
                filter_width = int(face_width * face_resize)
                filter_resize = resize(glasses, filter_width)
                filter_rotate = ndimage.rotate(filter_resize, degree+90)
                sY, sX, sD = filter_rotate.shape
                shift_x = sX//2
                shift_y = sY//2
                img_slice = img[eye_center[1]-shift_y:eye_center[1]-shift_y+sY, eye_center[0]-shift_x:eye_center[0]-shift_x+sX]
                print(img_slice.shape)
                print(filter_rotate.shape)
                blend_slice = blend_transparent(img_slice, filter_rotate)
                img[eye_center[1]-shift_y:eye_center[1]-shift_y+sY, eye_center[0]-shift_x:eye_center[0]-shift_x+sX] = blend_slice
                img_copy = img
            except BaseException as err:
                print(err)

            print("Done")
            return True, cv2.cvtColor(resize(img_copy, 1250), cv2.COLOR_BGR2RGB)

    except BaseException as err:
        print(err)

def take_pic(source):
    ret, img = source.read()
    if not ret:
        print("failed to grab frame")
        return

    img = resize(img, 700)
    img_copy = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #try:
    results = detect_faces(img, maxPeople=20, minConfidence=0.5)

    for face in results.multi_face_landmarks:
        #try:
            print(len(face.landmark))
            eye_left = get_left_eye(gray, face.landmark)
            eye_right = get_right_eye(gray, face.landmark)
            face_width = get_face_width(gray, face.landmark)
            x, y, w = get_box(gray, face.landmark)
            degree = np.rad2deg(np.arctan2(eye_left[0] - eye_right[0], eye_left[1] - eye_right[1]))

            eye_center = (eye_left[1] + eye_right[1]) / 2
            glasses_resize = resize(glasses, face_width)

            #Sunglasses translation
            #glass_trans = int(.2 * (eye_center - y))

            #Funny tanslation
            #glass_trans = int(-.3 * (eye_center - y ))

            # Mask translation
            glass_trans = int(-.2 * (eye_center - y))

            # Snap filter translation
            #glass_trans = int(-1.3 * (eye_center - y))

            yG, xG, cG = glasses_resize.shape
            glasses_resize_rotated = ndimage.rotate(glasses_resize, (degree+90))
            glass_rec_rotated = ndimage.rotate(img[y + glass_trans:y + yG + glass_trans, x:w], (degree+90))

            h5, w5, s5 = glass_rec_rotated.shape
            rec_resize = img_copy[y + glass_trans:y + h5 + glass_trans, x:x + w5 -1]
            blend_glass3 = blend_transparent(rec_resize , glasses_resize_rotated)
            img_copy[y + glass_trans:y + h5 + glass_trans, x:x+w5] = blend_glass3
            img = img_copy
            
        # except BaseException as err:
        #     print(err)
    cv2.imwrite("mediaTest.png", img_copy)
    print("Done")
    # except BaseException as err:
    #     print(err)

#MAIN
def main():
    while True:
        while True:
            ret, img = video_capture.read()
            if ret == True:
                cv2.imshow("Preview", img)
                if cv2.waitKey(1) & 0xFF == ord('y'):
                    break
                 
        #cv2.destroyAllWindows()
        take_pic_2()

if __name__ == "__main__":
    main()