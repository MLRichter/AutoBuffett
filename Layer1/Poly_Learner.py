# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 22:09:55 2016

This is a simple 'learner" which works on polynomial regression
The regression is done via a polynomial which is fittet onto a single 
epoch of datapoints
the last epoch is used to make the prediction of the next hundred  epoches

@author: Mats Richter
"""

import numpy as np

class Learner:
    #@input degree: degree of the polynomial
    #@input epoch: size of a single epoch of datapoints
    #@param tstep: discrete measurement of time
    #@param polynomial: poly1d object used for prediction
    #@☻param average return
    def __init__(self,degree=10,epoch=40000):
        self.degree = degree
        self.tstep = 0
        self.polynomial = None
        self.returns = list()
        self.epoch = epoch
        self.first = True
        self.std_returns = 1
        
    def predict(self,price1,price2):
        #add latest returns
        self.returns.append(price2-price1)
        #do nothing if not enough data was gathered
        if(self.tstep <= self.epoch):
            result = 0
        else:
            #if a epoch has ended, calculate the polynomal from the latest 
            #epoch
            if(self.tstep%(self.epoch) == 0 or self.first):
                self.polynomial = np.poly1d(np.polyfit(range(self.epoch),np.array(self.returns[(len(self.returns)-self.epoch):]),self.degree)) 
                self.std_returns = np.std(self.returns)
                self.first = False
            elif(self.tstep > self.epoch and self.tstep%(self.epoch/4) == 0):
                self.polynomial = np.poly1d(np.polyfit(range(self.epoch),np.array(self.returns[(len(self.returns)-self.epoch):]),self.degree)) 
                self.std_returns = np.std(self.returns)
            #receive latest prediction, normalization using the returns variance
            result = self.poly() / self.std_returns**2
        #increase t-step
        self.tstep += 1 
        #return prediction
        return np.tanh(result)
        
    def poly(self):
        #calculate the prediction of the polynomial-object
        return self.polynomial(self.tstep%self.epoch)