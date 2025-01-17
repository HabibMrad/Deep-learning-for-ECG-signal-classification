# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 21:00:54 2017

@author: Nancy
"""

from __future__ import print_function
# keras modules
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv1D, MaxPooling1D,Flatten
import numpy as np
from keras.callbacks import EarlyStopping  
import matplotlib.pyplot as plt
from keras.utils.vis_utils import plot_model
from keras import optimizers
from sklearn.metrics import confusion_matrix
#import matplotlib
#matplotlib.use('Agg')
from keras import backend as K
import os


os.environ['CUDA_VISIBLE_DEVICES'] = '1'

# plot ecg

import tensorflow as tf
import keras
def recall(y_true, y_pred):
        """Recall metric.

        Only computes a batch-wise average of recall.

        Computes the recall, a metric for multi-label classification of
        how many relevant items are selected.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

def precision(y_true, y_pred):
        """Precision metric.

        Only computes a batch-wise average of precision.

        Computes the precision, a metric for multi-label classification of
        how many selected items are relevant.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision

def f1(y_true, y_pred):
    def recall(y_true, y_pred):
        """Recall metric.

        Only computes a batch-wise average of recall.

        Computes the recall, a metric for multi-label classification of
        how many relevant items are selected.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

    def precision(y_true, y_pred):
        """Precision metric.

        Only computes a batch-wise average of precision.

        Computes the precision, a metric for multi-label classification of
        how many selected items are relevant.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision
    precision = precision(y_true, y_pred)
    recall = recall(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall))
class LossHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = {'batch':[], 'epoch':[]}
        self.accuracy = {'batch':[], 'epoch':[]}
        self.val_loss = {'batch':[], 'epoch':[]}
        self.val_acc = {'batch':[], 'epoch':[]}

    def on_batch_end(self, batch, logs={}):
        self.losses['batch'].append(logs.get('loss'))
        self.accuracy['batch'].append(logs.get('acc'))
        self.val_loss['batch'].append(logs.get('val_loss'))
        self.val_acc['batch'].append(logs.get('val_acc'))

    def on_epoch_end(self, batch, logs={}):
        self.losses['epoch'].append(logs.get('loss'))
        self.accuracy['epoch'].append(logs.get('acc'))
        self.val_loss['epoch'].append(logs.get('val_loss'))
        self.val_acc['epoch'].append(logs.get('val_acc'))

    def loss_plot(self, loss_type):
        iters = range(len(self.losses[loss_type]))
        plt.figure()
        # acc
        plt.plot(iters, self.accuracy[loss_type], 'r', label='train acc')
        # loss
        plt.plot(iters, self.losses[loss_type], 'g', label='train loss')
        if loss_type == 'epoch':
            # val_acc
            plt.plot(iters, self.val_acc[loss_type], 'b', label='val acc')
            # val_loss
            plt.plot(iters, self.val_loss[loss_type], 'k', label='val loss')
        plt.grid(True)
        plt.xlabel(loss_type)
        plt.ylabel('acc-loss')
        plt.legend(loc="upper right")
        #plt.convert('RGB')
        plt.savefig('epoch_1d.png')
        #plt.show()
# for loading data
import scipy.io

#check version of tf and k
print('tf version is', tf.__version__)
print('keras version is', keras.__version__)

# load ECG data
#data = scipy.io.loadmat('one_dim.mat')
data = scipy.io.loadmat('/home/liuying/ecg_Keras/oneDoriginal.mat')
#data = scipy.io.loadmat('C:/Users/lab/Desktop/one_dimen.mat')
# test set
x_test = data['x_test']
x_test = np.expand_dims(x_test, axis=2)
y_test = data['y_test']

# training set
x_train = data['x_train']
x_train = np.expand_dims(x_train, axis=2)
y_train = data['y_train']

# free up memory
del(data)

print(len(x_train), 'training examples')
print(len(x_test), 'test examples')

print('x_train shape is', x_train.shape)
print('x_test shape is', x_test.shape)

# plot a ecg for checking
#plt.figure('ecg')
#plt.plot(range(820),np.squeeze(x_train[101,:,:]))




# hyper parameters in ConNets
hidden_dims = 100
batch_size = 32
epochs =100
# model
print('Building model...')
model = Sequential()
 
model.add(Conv1D(32,7,strides=3,input_shape=(820,1),padding='valid',activation='relu',
                 kernel_initializer='uniform',
                 kernel_regularizer=keras.regularizers.l2(0.01)))  
model.add(MaxPooling1D(pool_size=3,strides=2))  
model.add(Conv1D(64,5,strides=1,padding='same',activation='relu',
                 kernel_initializer='uniform'))  
model.add(MaxPooling1D(pool_size=3,strides=2)) 
model.add(Conv1D(128,3,strides=1,padding='same',activation='relu',
                 kernel_initializer='uniform'))  
model.add(Conv1D(128,3,strides=1,padding='same',activation='relu',
                 kernel_initializer='uniform')) 
model.add(Conv1D(128,3,strides=1,padding='same',activation='relu',
                 kernel_initializer='uniform')) 
model.add(MaxPooling1D(pool_size=3,strides=2))  
model.add(Flatten())  
model.add(Dense(4096,activation='relu'))  
model.add(Dropout(0.5))  
model.add(Dense(4096,activation='relu'))  
model.add(Dropout(0.5))  
model.add(Dense(1,activation='sigmoid'))  

#sgd=optimizers.SGD(lr=0.01,decay=1e-6,momentum=0.9,nesterov=True)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=[recall])
history = LossHistory()
#early_stopping =EarlyStopping(monitor='acc', min_delta=0.0001,patience=5,mode='max')
model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs,shuffle=True,validation_data=(x_test, y_test),callbacks=[history])
THRESHOLD = 0.5
y_pred=(model.predict(x_test) >= THRESHOLD).astype(int)
y_true=y_test
conf_mat = confusion_matrix(y_true, y_pred)
print(conf_mat)
#score = model.evaluate(x_test, y_test, verbose=0)
#print('Test loss:', score[0])
#print('Test accuracy:', score[1])
plot_model(model, to_file='model_1d.png') 
#history.loss_plot('epoch')
history.on_train_begin('acc')
model.summary()
