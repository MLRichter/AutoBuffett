# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 22:20:56 2016

This is a linear, recurrent SVM learning in batch mode
The system receives every timestep a single return by the system and 
returns on a prediction within range [-1 1]
The system uses a linear SVM
The labels are defined by the sharpé ratio over a sliding window 

@author: Mats Richter
"""

from sklearn import linear_model
import numpy as np
import RNJesus as rnj

class Learner:
       
       #@input recurrence: Dimensionality of the feature-space
       #        with dimension corresponding to the last n returns
       #        this is a positive integer
       #@input realy_recurrent: default=False
       #        if true: the last decision is also a dimension in the
       #        feature space
       #@input label_par paramter used for labeling 'r' for returns
       #                                            'p' for prices
    def __init__(self,adaption = 0.5,transactionCost = 0.001, recurrence=35, realy_recurrent=False, w_size=20,label_par='r'):
        self.learner = linear_model.SGDClassifier(n_jobs=-1)
        self.transactionCost = transactionCost
        self.adaption = adaption
        
        #size of each training batch
        self.batch_size = w_size * (recurrence)
        #size of the sliding window for sharpé ratio
        self.window_size = 20 * self.batch_size
        
        # the data matrix of a single batch
        # Data-Vector = r_1, ... r_n, prediction_t-1
        # with r_n := r_n - r_n-1
        self.returns = list()
        self.labels = list()
        self.decisions = [0]
        self.weighted_returns = list()
        
        self.rng = rnj.Learner()
        
        self.recurrence = recurrence
        self.last_decision = 0
        self.ready = False
        self.tstep = 0
        self.recurrent = realy_recurrent
        #self.prices = list()
        self.label_par = label_par
        
        self.sharpeA_old = 1
        self.sharpeB_old = 1
        return
        
    def predict(self,new_price,old_price,tstep = 0):
        latest_return = new_price - old_price

        #Test differen classifier
        #if(self.tstep == 0):
        #    self.prices.append(old_price)
        #self.prices.append(new_price)
        #if(len(self.prices) > self.window_size):
        #    self.prices.pop(0)

        self.tstep += 1
        self.returns.append(latest_return)
        if(self.ready):
            x = self.returns[len(self.returns)-self.recurrence-1:len(self.returns)-1]
            if(self.recurrent):
                x.append(self.last_decision)            
            x = np.array(x)
            x = x.reshape((len(x),1))
            x = np.transpose(x)
            #maybe add previous decision later on
            decision = np.tanh(self.learner.decision_function(x))
        else:
            decision = 1#self.rng.predict()
        self.weighted_returns.append(self.last_decision * latest_return - (self.transactionCost*np.fabs(self.last_decision - decision)))
        if(self.tstep > self.window_size):
            if(len(self.returns) > self.window_size):
                self.returns.pop(0)
                self.weighted_returns.pop(0)
        if(self.tstep%self.batch_size == 0 and self.tstep != 0):
            self.train()
            self.ready = True
        self.decisions.append(decision)
        if(len(self.decisions) > self.window_size):
            self.decisions.pop(0)
        self.last_decision = decision
        return  decision
    
    #calls partial_fit() on the svm to adjust it's internal model
    def train(self):
        returns = np.array(self.returns)
        returns = returns[len(returns)-(self.batch_size):]
#        returns = returns.reshape((100,self.recurrence))
        
        weighted_returns = np.array(self.returns)
        weighted_returns = weighted_returns[len(weighted_returns)-(self.batch_size):]
       #weighted_returns = weighted_returns.reshape((100,self.recurrence))
        
        decisions = np.array(self.decisions)
        decisions = decisions[len(decisions)-(self.batch_size):]
        #decisions = decisions.reshape((100,self.recurrence))
        
        trainingMatrix = list()
        self.label = list()
        
        for i in range(self.recurrence,len(weighted_returns)-2):
            trainDat = weighted_returns[i-self.recurrence:i]
            self.labels.append(self.label_util(trainDat[:self.recurrence-1],decisions[i+1],self.weighted_returns[i+1],self.weighted_returns[i]))
            trainingMatrix.append(returns[i-self.recurrence:i])
       # try:  
        #print np.shape(trainingMatrix)
        #print np.shape(self.labels)
        self.learner.partial_fit(trainingMatrix, self.labels, classes=[-1,1])
        #except:
        self.labels = list()
        return
        #calls partial_fit() on the svm to adjust it's internal model
        
    #labeling function using the complete vector
    def label_set(self,return_list,decision_list):
        if np.mean(return_list) < 0:
            if np.mean(decision_list) < 0:
                return -1
            else:
                return 1
        else:
            if np.mean(decision_list) < 0:
                return 1
            else:
                return -1
    
    #alternative (and highly experiment)function for labeling       
    def label_util(self,return_list,decision,proto_label = 1,latest = 1, c = 1):
        #init sharpe Ratio if not yet initilized
        if(self.sharpeA_old == 1):
            sharpeA = np.mean(self.weighted_returns)
            sharpeB = np.std(self.weighted_returns)
        else:
            #iterative calculation of the ratio
            sharpeA = self.sharpeA_old + self.adaption*(latest - self.sharpeA_old)
            sharpeB = self.sharpeB_old + self.adaption*((latest**2) - self.sharpeB_old)
        # Bachelor performance measure
       # performance = (sharpeB*(proto_label - sharpeA)) - (sharpeA * (proto_label**2 - sharpeB))
       # performance /= ((sharpeB - (sharpeA ** 2)) ** (3 / 2))
        #Performance Measure exp1
        #performance = (sharpeB*(proto_label) - (sharpeA * (proto_label**2)))
        #performance /= ((sharpeB - (sharpeA ** 2)) ** (3 / 2))
        performance = (sharpeB*(proto_label - (c*sharpeA)) - (proto_label * (proto_label**2 - (c*sharpeB))))
        performance /= ((sharpeB - (proto_label ** 2)) ** (3 / 2))        
        self.sharpeA_old = sharpeA
        self.sharpeB_old = sharpeB
        
        if(performance < 0):
            if decision <= 0:
                return 1
            else:
                return -1
        else:
            if decision < 0:
                return -1
            else:
                return 1
                
    def label_last(self,return_list,decision_list):
        if return_list[len(return_list)-1] < 0:
            if decision_list[len(return_list)-1] < 0:
                return 1
            else:
                return -1
        else:
            if decision_list[len(return_list)-1] < 0:
                return -1
            else:
                return 1
            
        