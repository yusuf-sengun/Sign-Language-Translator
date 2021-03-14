# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 10:46:08 2021

@author: olgun
"""
import cv2
import numpy as np
# How to load and use weights from a checkpoint
from tensorflow.keras.layers import Flatten,Dense,Dropout,MaxPooling2D,Conv2D,BatchNormalization
from keras.models import Sequential
from keras.preprocessing.image import img_to_array
import numpy
from matplotlib import pyplot as plt
from PIL import Image
import pandas as pd

cnn_model = Sequential()

cnn_model.add(Conv2D(32, (3, 3), input_shape = (28,28,1), activation='relu'))
cnn_model.add(MaxPooling2D(pool_size = (2, 2)))
cnn_model.add(Dropout(0.25))

cnn_model.add(Conv2D(64, (3, 3), input_shape = (28,28,1), activation='relu'))
cnn_model.add(MaxPooling2D(pool_size = (2, 2)))
cnn_model.add(Dropout(0.25))

cnn_model.add(Conv2D(128, (3, 3), input_shape = (28,28,1), activation='relu'))
cnn_model.add(MaxPooling2D(pool_size = (2, 2)))
cnn_model.add(Dropout(0.25))

cnn_model.add(Flatten())

cnn_model.add(Dense(units = 512, activation = 'relu'))
cnn_model.add(Dropout(0.25))
cnn_model.add(Dense(units = 25, activation = 'softmax'))

cnn_model.compile(loss ='sparse_categorical_crossentropy', optimizer='adam' ,metrics =['accuracy'])


filepath=r"C:\Users\olgun\Desktop\Sign Language Translator\weights.best.hdf5"
cnn_model.load_weights(filepath)
print("Created model and loaded weights from file")



def take_letter(index):
    class_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y' ]
    return class_names[index]

def keras_predict(model, image):
    processed = keras_process_image(image)
    pred_probab = model.predict(processed)[0]
    pred_class = list(pred_probab).index(max(pred_probab))
    return max(pred_probab), pred_class,take_letter(pred_class)

def keras_process_image(img):
    image_x = 28
    image_y = 28
    img = cv2.resize(img, (image_x, image_y))
    img2=cv2.resize(img,(100,100))
    cv2.imshow('gonderilen',img2)
    img_array = img_to_array(img)
    img_array=img_array/255
    #img = np.array(img, dtype=np.uint8)
    img_array = img_array.reshape(-1,28, 28, 1)
    print(img_array)
    return img_array

def runFingerCounter():
    cap = cv2.VideoCapture(0)
    start_point=(300,300)
    end_point=(100,100)
    color=(0,255,0)
    thickness=0

    while (cap.isOpened()):
        ret, img = cap.read()
        #img = cv2.flip(img, 1)
        
        
        cv2.rectangle(img,start_point,end_point,color,thickness)
        crop_img=img[end_point[0]:start_point[0],end_point[0]:start_point[0]]
        
        hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
        lower_skin = np.array([0,58,50], dtype=np.uint8)
        upper_skin = np.array([30,255,255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        #res = cv2.bitwise_and(crop_img,crop_img, mask= mask)
        
        kernel = np.ones((5,5),np.uint8)
        mask = cv2.dilate(mask,kernel,iterations = 2)

        #mask = cv2.adaptiveThreshold(mask,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        blur = cv2.GaussianBlur(mask,(5,5),0)
        _,mask = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
        #thresholding: Binarization method(Adaptive thresholding de olabilir)
        contours,hierarchy=cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #find max contour with max area.
        if len(contours) > 0:
            cnt= max(contours,key=lambda x: cv2.contourArea(x))
            if cv2.contourArea(cnt) > 2500: 
                x, y, w1, h1 = cv2.boundingRect(cnt)
                pred_probab, pred_class,letter = keras_predict(cnn_model, mask)
                cv2.putText(img,letter,(0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3, cv2.LINE_AA)
                cv2.putText(img,"%"+str(round(pred_probab,2)*100),(2,90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
        cv2.imshow('Frame',img)
        cv2.imshow('hsv',hsv)
        cv2.imshow("Mask", mask)
        k = cv2.waitKey(10)
        if k == 'q':
            cv2.destroyAllWindows()
            break 
runFingerCounter()


    

