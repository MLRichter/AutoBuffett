# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 13:39:12 2016

Multi-Layer-Perceptron as Learner

@author: Mats Richter
"""

import numpy as np
import sknn.mlp as mlp

class Learner:
    
    #@input w_size: size of the sliding window used for batch learning
    #@input size:   numbers of parameters fed in the input layer
    #@input mode:   switch between processing returns or prices 
    #
    #@param learner: A MLP-Regressor for learning
    #@param data:    The data fed into the system
    def __init__(self,w_size=100,input_size=12,mode='returns',layers=1,n_itr=50,learn=0.05,AutoEncoder=False):
        self.layers = list()   
        #setup layers HIGHLY TENTETIVE AND SUBJECT TO CHANGE
        for i in range(layers):
            layer = mlp.Layer('Rectifier',units=input_size)
            self.layers.append(layer)
        self.layers.append(mlp.Layer('Linear'))
        self.learner = mlp.Regressor(self.layers,learning_rate=learn,n_iter=n_itr)
        self.input_size = input_size
        self.w_size = self.input_size * w_size
        self.data = list()
        self.tstep = 0
        self.mode = mode
        
        self.std = 1
        return
        
    def predict(self,price1,price2):
        result = 0
        #add data to the data-vector
        if(self.mode == 'returns'):
            self.data.append(np.float32(price2-price1))
        elif(self.mode == 'prices'):
            if(len(self.data) == 0):
                self.data.append(price1)
            self.data.append(price2)
        if(len(self.data)> self.w_size):
            self.data.pop(0)

        if(self.learner.is_initialized):
            #setup input vector:
            x = self.data[len(self.data)-self.input_size-1:len(self.data)-1]
            x = np.array(x)
            x = x.reshape((len(x),1))
            x = np.transpose(x)
            pred = self.learner.predict(x)
            pred = pred[0][0]
            #calculate result depending on settings
            #the variance of the data is used as normalizing factor to 
            #highlight the changes in the tanh-function more
            if(self.mode == 'returns'):
                result = np.tanh(pred * (1/self.std))#**2))
                #return pred
            elif(self.mode == 'prices'):
                #result = np.tanh((pred - price2)/(self.std**2))
                result = pred
            else:
                result = 0
        #if window is full, start training
        if(self.tstep%self.w_size == 0 and self.tstep != 0):
            self.train()
            #clear window
        self.tstep += 1
        return result
    
        
    def train(self):
        #arrange data for processing
        #print("starting training...")
        data = np.array(self.data)
        #data = data.reshape(len(data),1)
        #data = np.transpose(data)
        #setup label vector and data matrix
        dat_matrix = list()
        labels = list()
        #construct datamatrix and labels
        for i in range(len(self.data)-self.input_size-2):
            #input data are the previous results
            dat_matrix.append(data[i:(i+self.input_size)])
            #labels result directly after the input-series
            labels.append(data[i+self.input_size+1])
        dat_matrix = np.array(dat_matrix)
        #dat_matrix = np.transpose(dat_matrix)
        labels = np.array(labels)
        #labels = labels.reshape((len(labels),1))
        #labels = np.transpose(labels)
        #dat_matrix = np.transpose(dat_matrix)
        self.learner.fit(dat_matrix,labels)
        self.std = np.std(self.data)
#        print("training done")
        return  