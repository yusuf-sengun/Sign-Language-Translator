# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 21:40:52 2021

@author: olgun
"""
import pandas as pd
import numpy as np

train = pd.read_csv(r'C:\Users\olgun\Desktop\SEProject\Dataset\sign_mnist_train.csv')
test = pd.read_csv(r'C:\Users\olgun\Desktop\SEProject\Dataset\sign_mnist_test.csv')

train_set = np.array(train, dtype = 'float32')
test_set = np.array(test, dtype='float32')


#Normalization for pixels of images.
#Our CNN model will make the model run faster
#X_train represents our images pixel

X_train = train_set[:, 1:] / 255
X_test = test_set[:, 1:] / 255

y_train = train_set[:, 0]
y_test = test_set[:,0]


#Split the training, test and validation data.
from sklearn.model_selection import train_test_split
X_train, X_validate, y_train, y_validate = train_test_split(X_train, y_train, test_size = 0.2, random_state = 12345)


img_width=28
img_height=28
#reshape the data for keras model(-1,28,28,1 format.)
X_train = X_train.reshape(X_train.shape[0], *(img_width, img_height, 1))
X_test = X_test.reshape(X_test.shape[0], *(img_width, img_height, 1))
X_validate = X_validate.reshape(X_validate.shape[0], *(img_width, img_height, 1))


from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout


#Defining the Convolutional Neural Network
cnn_model = Sequential()

kernel=(3,3)
cnn_model.add(Conv2D(64, kernel, input_shape = (28,28,1), activation='relu'))
cnn_model.add(MaxPooling2D(pool_size = (2, 2)))
cnn_model.add(Dropout(0.25))

cnn_model.add(Conv2D(128, kernel, input_shape = (28,28,1), activation='relu'))
cnn_model.add(MaxPooling2D(pool_size = (2, 2)))
cnn_model.add(Dropout(0.25))

cnn_model.add(Conv2D(256, kernel, input_shape = (28,28,1), activation='relu'))
cnn_model.add(MaxPooling2D(pool_size = (2, 2)))
cnn_model.add(Dropout(0.25))

cnn_model.add(Flatten())

cnn_model.add(Dense(units = 512, activation = 'relu'))
cnn_model.add(Dropout(0.25))
cnn_model.add(Dense(units = 25, activation = 'softmax'))

#Compile and save the weights.
from keras.callbacks import ModelCheckpoint

cnn_model.compile(loss ='sparse_categorical_crossentropy', optimizer='adam' ,metrics =['accuracy'])
filepath=r"C:\Users\olgun\Desktop\SEProject\Dataset\weights.best.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]
#Training the CNN model
history = cnn_model.fit(X_train, y_train, batch_size = 512, epochs = 50, verbose = 1, validation_data = (X_validate, y_validate),callbacks=callbacks_list)

predicted_classes=cnn_model.predict_classes(X_test)
cnn_model.evaluate(X_test,predicted_classes)


