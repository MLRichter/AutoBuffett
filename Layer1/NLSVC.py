# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 09:59:57 2016

nonlinear Support Vector Mashine

@author: Mats Richter
"""

from sklearn.svm import NuSVC
import numpy as np

class Learner:
       
       #@input recurrence: Dimensionality of the feature-space
       #        with dimension corresponding to the last n returns
       #        this is a positive integer
       #@input realy_recurrent: default=False
       #        if true: the last decision is also a dimension in the
       #        feature space
       #@input label_par paramter used for labeling 'r' for returns
       #                                            'p' for prices
    def __init__(self, recurrence=30, w_size=20,hybrid = False):
        self.learner = NuSVC()
        
        #size of each training batch
        self.batch_size = w_size * (recurrence)
        #size of the sliding window for sharpé ratio
        self.window_size = 5 * self.batch_size
        
        #true if part of a hybrid learner
        self.hybrid = hybrid
        
        # the data matrix of a single batch
        # Data-Vector = r_1, ... r_n
        # with r_n := r_n - r_n-1
        self.returns = list()
        #training data for experimental apporach
        self.train_dat = list()
        self.labels = list()
        self.decisions = list()
        self.recurrence = recurrence
        
        self.last_decision = 0
        self.ready = False
        self.tstep = 0
        self.prices = list()
        return
       
    def predict(self,new_price,old_price,tstep = 0):
        #default decision value        
        decision = 0
        #Add prices to sliding window
        self.prices.append(new_price)
        if(len(self.prices) > self.window_size):
            self.prices.pop(0)
        latest_return = new_price - old_price
        #add next label
        if(self.tstep > self.recurrence):
            self.labels.append(self.label_returns(latest_return))
        #increment timer
        self.tstep += 1
        #add latest return to history
        self.returns.append(latest_return)
        if(self.tstep > self.window_size):
            if(len(self.returns) > self.window_size):
                self.returns.pop(0)
        #if batch is full, start training
        if(self.tstep%self.batch_size == 0 and self.tstep != 0):
            self.train()
            #disabled this, normally for predicting prices, but performance is
            #worse, so this is actually dead code
        #setup x-vector
        if(self.tstep > self.recurrence):
            x = self.returns[len(self.returns)-self.recurrence-1:len(self.returns)-1]
            #set up training matrix            
            x = np.array(x)
            x = x.reshape((len(x),1))
            self.train_dat.append(x)
            x = np.transpose(x)
            #create decision only if svm is trained
            if(self.ready):
                decision = np.tanh(self.learner.decision_function(x))
                decision = decision[0]
        #if the system is truly recurrent (uses the last decision input-vecotr)
        #append the decision
        self.last_decision = decision
        return  decision
    
    #calls partial_fit() on the svm to adjust it's internal model
    def train(self):
        #setup training matrix
        train_dat = np.zeros((len(self.labels),self.recurrence))
        for i in range(len(train_dat)):
            train_dat[i][:] = np.transpose(self.train_dat[i])
        #np.transpose(train_dat)
        self.learner.fit(train_dat, self.labels)
        #clear the training-related strzctures
        self.labels = list()
        self.train_dat = list()
        self.ready = True
        return
        #calls partial_fit() on the svm to adjust it's internal model
        
    #labeling function using the complete vector
    #very simple, since it only detects trends depending on the mu
    def label_set(self,return_list):
        mu_current = np.mean(return_list)
        mu_total = np.mean(self.returns)
        if(mu_current >= mu_total):
            return 1
        else:
            return -1
            
    def label_returns(self,next_return):
        if next_return > 0:
            return 1
        else:
            return -1