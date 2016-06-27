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
    def __init__(self,w_size=100,input_size=12,layers=1,n_itr=50,learn=0.05,AutoEncoder=False,adaption = 0.1):
        self.layers = list()   
        #setup layers HIGHLY TENTETIVE AND SUBJECT TO CHANGE
        for i in range(layers):
            layer = mlp.Layer('Rectifier',units=input_size)
            self.layers.append(layer)
        self.layers.append(mlp.Layer('Softmax'))
        self.learner = mlp.Classifier(self.layers,learning_rate=learn,n_iter=n_itr)
        self.input_size = input_size
        self.w_size = self.input_size * w_size
        self.data = list()
        self.returns = list()
        self.labels = list()
        self.tstep = 0
        
        self.sharpeA = 1
        self.sharpeB = 1
        self.adaption = adaption
        
        self.std = 1
        return
        
    def predict(self,price1,price2):
        result = 0
        #add data to the data-vector
        self.returns.append(price2-price1)
        if(len(self.data)> self.w_size):
            self.returns.pop(0)
        #build input-vector if enought data is available
        if(self.tstep > self.input_size):
            #label returns
            self.labels.append(self.label_returns(price2-price1))
            #init data vector
            x = list()
            #setup input vector:
            x = self.returns[len(self.returns)-self.input_size-1:len(self.returns)-1]
            x = np.array(x)
            x = x.reshape((len(x),1))
            self.data.append(x)
            x = np.transpose(x)
            if(self.learner.is_initialized):
                self.update_sharpe(price2-price1)
                #predict the probability of each class
                pred = self.learner.predict_proba(x)
                #prepare output for return
                if(pred[0][0] < pred[0][1]):
                    result = pred[0][0]
                else:
                   result = pred[0][1] * (-1)
                    
            else:
                result = 0
        #if window is full, start training
        if(self.tstep%self.w_size == 0 and self.tstep != 0):
            self.train()
            self.is_initialized = True
            #clear window
        self.tstep += 1
        return np.tanh(result * np.fabs(self.sharpeA/self.sharpeB))
        
    def train(self):
        #arrange data for processing
        data = np.array(self.data)
        train_dat = np.zeros((len(self.labels),self.input_size))
        for i in range(len(train_dat)):
            train_dat[i][:] = np.transpose(self.data[i])
        
        self.learner.fit(train_dat,np.array(self.labels))
        self.std = np.std(self.data)
        #print("training done")
        #clear data and labels
        self.data = list()
        self.labels = list()
        return  
        
    def label_returns(self,next_return):
        if next_return > 0:
            return 1
        else:
            return -1
            
    def update_sharpe(self,latest_return):
        self.sharpeA += self.adaption*(latest_return - self.sharpeA)
        self.sharpeB += self.adaption*(latest_return**2 - self.sharpeB)