# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 18:10:15 2018

@author: luisxavierramostormo
"""
import numpy as np

import keras
from keras import Sequential
from keras import backend as K
from keras.layers import Dense, Conv2D, MaxPooling2D, SpatialDropout2D, Flatten
from keras.layers import BatchNormalization, Dropout

# keras docs: https://keras.io

from wig_extractor.py import load_training_data


class chrom_CNN(object):
    def __init__(self):
        self.batch_size = 128
        self.epochs = 12
        
        # input dimensions
        self.img_rows, self.img_cols = 1, 800 # second number can be any
        (self.x_train, self.y_train), (self.x_test, y_test) = load_training_data()
        
        if K.image_data_format() == 'channels_first':
            self.x_train = self.x_train.reshape(self.x_train.shape[0], 1, self.img_rows, self.img_cols)
            self.x_test = self.x_test.reshape(self.x_test.shape[0], 1, self.img_rows, self.img_cols)
            self.input_shape = (1, self.img_rows, self.img_cols)
        else:
            self.x_train = self.x_train.reshape(self.x_train.shape[0], self.img_rows, self.img_cols, 1)
            self.x_test = self.x_test.reshape(self.x_test.shape[0], self.img_rows, self.img_cols, 1)
            self.input_shape = (self.img_rows, self.img_cols, 1)

        self.x_train = self.x_train.astype('float32')
        self.x_test = self.x_test.astype('float32')
        print('x_train shape:', self.x_train.shape)
        print(self.x_train.shape[0], 'train samples')
        print(self.x_test.shape[0], 'test samples')
        
        model = Sequential()
        model.add(Conv2D(32, kernel_size=(1, 9),
                         activation='relu',
                         input_shape=self.input_shape))
        model.add(Conv2D(64, (1, 9), activation='relu'))
        model.add(MaxPooling2D(pool_size=(1, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.img_cols, activation='tanh')) # tanh is the kind of output we want. Between 0 and 1 and stronger gradients than sigmoid
        
        model.compile(loss=keras.losses.categorical_crossentropy,
                      optimizer=keras.optimizers.Adadelta(),
                      metrics=['accuracy']) # TODO change metrics
        
        model.fit(self.x_train, self.y_train,
                  batch_size=self.batch_size,
                  epochs=self.epochs,
                  verbose=1,
                  validation_data=(self.x_test, self.y_test))
        score = model.evaluate(self.x_test, self.y_test, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])

