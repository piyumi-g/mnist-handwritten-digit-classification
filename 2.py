# -*- coding: utf-8 -*-
"""2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nFiZSeCsJ8cbwvQRZ61LxCzSiW4coZkj
"""

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

#parameters
batch_size = 32
num_classes = 10
epochs = 10
(x_train, y_train), (x_test, y_test) = mnist.load_data()

print(np.shape(x_train))
print(np.shape(y_train))
print(np.shape(x_test))
print(np.shape(y_test))

#Image dataset dimensions
img_rows, img_cols = 28, 28
print(img_rows, img_cols)

#Reshape the dataset to have a single colour channel
x_train = x_train.reshape((x_train.shape[0], img_rows, img_cols, 1))
x_test = x_test.reshape((x_test.shape[0], img_rows, img_cols, 1))

#One hot encode target values
from keras.utils import to_categorical

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

#Convert from integers to floats to divide the pixel value from the max value
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

# normalize to range 0-1
x_train = x_train / 255.0
x_test = x_test / 255.0

print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')


#Creating the model
from keras.optimizers import SGD

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)))
model.add(MaxPooling2D((2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

#Compile model
optimizer = SGD(lr=0.01, momentum=0.9)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

"""**Adding Random Noise**"""

noise_factor = 0.25

x_train_noisy = x_train + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_train.shape)
x_test_noisy = x_test + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_test.shape)
#y_train_noisy = np.clip(x_train_noisy, 0., 1.)
#y_test_noisy = np.clip(x_test_noisy, 0., 1.)


y_train_noisy = y_train + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=y_train.shape)
y_test_noisy = y_test + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=y_test.shape)

print(np.shape(x_train_noisy))
print(np.shape(y_train_noisy))
print(np.shape(x_test_noisy))
print(np.shape(y_test_noisy))

#running the model again with noise
model.fit(x_train_noisy, y_train_noisy,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test_noisy, y_test_noisy))

score = model.evaluate(x_test_noisy, y_test_noisy, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
print('> %.3f' % (score[1] * 100.0))