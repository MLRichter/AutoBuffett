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
    def __init__(self,adaption = 0.5,transactionCost = 0.001, recurrence=35, realy_recurrent=False, w_size=20,label_par='r'):
        self.learner = NuSVC()
        self.transactionCost = transactionCost
        self.adaption = adaption
        
        #size of each training batch
        self.batch_size = 200 * (recurrence)
        #size of the sliding window for sharpé ratio
        self.window_size = w_size * self.batch_size
        
        # the data matrix of a single batch
        # Data-Vector = r_1, ... r_n, prediction_t-1
        # with r_n := r_n - r_n-1
        self.returns = list()
        self.labels = list()
        self.decisions = [0]
        self.weighted_returns = list()
        
        #self.rng = rnj.Learner()
        
        self.recurrence = recurrence
        self.last_decision = 0
        self.ready = False
        self.tstep = 0
        self.recurrent = realy_recurrent
        self.prices = list()
        self.label_par = label_par
        
        self.sharpeA_old = 1
        self.sharpeB_old = 1
        return
        
    def predict(self,new_price,old_price,tstep = 0):
        latest_return = new_price - old_price

        #Test differen classifier
        #if(self.tstep == 0):
        #    self.prices.append(old_price)
        self.prices.append(new_price)

        if(len(self.prices) > self.window_size):
            self.prices.pop(0)

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
            decision = 0.5#self.rng.predict()
        self.weighted_returns.append(self.last_decision * latest_return - (self.transactionCost*np.fabs(self.last_decision - decision)))
        if(self.tstep > self.window_size):
            if(len(self.returns) > self.window_size):
                self.returns.pop(0)
        if(self.tstep%self.batch_size == 0 and self.tstep != 0 and self.tstep%self.window_size==0):
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
        
        weighted_returns = np.array(self.weighted_returns)
        weighted_returns = weighted_returns[len(weighted_returns)-(self.batch_size):]
       #weighted_returns = weighted_returns.reshape((100,self.recurrence))
        
        decisions = np.array(self.decisions)
        decisions = decisions[len(decisions)-(self.batch_size):]
        #decisions = decisions.reshape((100,self.recurrence))
        
        trainingMatrix = list()
        self.labels = list()
        
        #for i in range(len(weighted_returns)):
            #self.labels.append(self.label_set(weighted_returns[i],decisions[i]))
        for i in range(self.recurrence,len(weighted_returns)-1):
            trainDat = weighted_returns[i-self.recurrence:i]
            self.labels.append(self.label_util(trainDat[:self.recurrence-1],decisions[i]))
            trainingMatrix.append(returns[i-self.recurrence:i])
            #trainingMatrix.append(trainDat)
            
        #new_returns = np.zeros((100,self.recurrence+1))
        #new_returns[:,:-1] = returns
        #decisions = np.array(self.labels)
        #decisions = decisions.reshape(len(decisions),1)
       # new_returns[:,self.recurrence-1] = np.transpose(decisions)
        #if(self.recurrent):
            #self.learner.partial_fit(new_returns, self.labels, classes=[-1,1])
        #else:
        #    self.learner.partial_fit(returns, self.labels, classes=[-1,1])
        self.learner.fit(trainingMatrix, self.labels)
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
    def label_util(self,return_list,decision):
        
        if(self.sharpeA_old == 1):
            sharpeA = np.mean(self.weighted_returns)
            sharpeB = np.std(self.weighted_returns)
        else:
            sharpeA = self.sharpeA_old + self.adaption*(return_list[len(return_list)-1] - self.sharpeA_old)
            sharpeB = self.sharpeB_old + self.adaption*((return_list[len(return_list)-1]**2) - self.sharpeB_old)
        
        performance = (sharpeB - (return_list[len(return_list)-1] - self.sharpeA_old)) - (sharpeA * (return_list[len(return_list)-1]**2 - self.sharpeB_old))
        performance /= ((sharpeB - (sharpeA ** 2)) ** (3 / 2))
        self.sharpeA_old = sharpeA
        self.sharpeB_old = sharpeB
        
        if(performance < 0):
            if decision < 0:
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