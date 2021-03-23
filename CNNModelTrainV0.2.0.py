# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 23:54:57 2021

@author: olgun
"""

import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Conv2D , MaxPool2D , Flatten , Dropout , BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ReduceLROnPlateau


train_df=pd.read_csv(r"C:\Users\olgun\Desktop\SEProject\Dataset\sign_mnist_train.csv")
test_df=pd.read_csv(r"C:\Users\olgun\Desktop\SEProject\Dataset\sign_mnist_test.csv")
label_train=train_df['label']#A->0, B-> 1
label_test=test_df['label']# A->0 , B-> 1

del train_df['label']
del test_df['label']


from sklearn.preprocessing import LabelBinarizer

label_binarizer=LabelBinarizer()

label_train=label_binarizer.fit_transform(label_train)
label_test=label_binarizer.fit_transform(label_test)

values_train=train_df.values
values_test=test_df.values


#Normalize the data
#we perform normalization, CNN model works faster.
values_train=values_train/255
values_test=values_test/255

#Keras needs an extra dimension in the end which correspond to channels. Our images are gray scaled so it use only one channel.
values_train=values_train.reshape(-1,28,28,1)
values_test=values_test.reshape(-1,28,28,1)

datagen = ImageDataGenerator(
    width_shift_range=[-200,200],#kayma miktarı yatayda
    height_shift_range=[-200,200],#kayma miktarı dikeyde
    featurewise_center=True,
    horizontal_flip = True,
    vertical_flip=True,
    rotation_range=[0,180],
    brightness_range=[0.1,1.5],
    zoom_range=[0.1,1.5],
    shear_range =[0.1,1.5], 
    )
datagen.fit(values_train)
learning_rate_reduction = ReduceLROnPlateau(monitor='val_accuracy', patience = 2, verbose=1,factor=0.5, min_lr=0.00001) 

model = Sequential()
model.add(Conv2D(75 , (3,3) , strides = 1 , padding = 'same' , activation = 'relu' , input_shape = (28,28,1)))
model.add(Dropout(0.25))
model.add(BatchNormalization())
model.add(MaxPool2D((2,2) , strides = 2 , padding = 'same'))

model.add(Conv2D(50 , (3,3) , strides = 1 , padding = 'same' , activation = 'relu'))
model.add(Dropout(0.25))
model.add(BatchNormalization())
model.add(MaxPool2D((2,2) , strides = 2 , padding = 'same'))

model.add(Conv2D(25 , (3,3) , strides = 1 , padding = 'same' , activation = 'relu'))
model.add(Dropout(0.25))
model.add(BatchNormalization())
model.add(MaxPool2D((2,2) , strides = 2 , padding = 'same'))

model.add(Flatten())
model.add(Dense(units = 512 , activation = 'relu'))
model.add(Dropout(0.30))
model.add(Dense(units = 24 , activation = 'softmax'))

model.compile(optimizer = 'adam' , loss = 'categorical_crossentropy' , metrics = ['accuracy'])


from keras.callbacks import ModelCheckpoint
filepath=r"C:\Users\olgun\Desktop\SignLanguageProject\best.weights.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]
#Training the CNN model
history = model.fit(values_train, label_train, batch_size = 256 , epochs = 50, verbose = 1, validation_data = (values_test, label_test),callbacks=[callbacks_list,learning_rate_reduction])

