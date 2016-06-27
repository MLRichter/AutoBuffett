# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 23:40:56 2016

A wrapper-like learner which basically wire a svm and a rll system on top of 
each other to create a hybrid learning system.

@author: Mats Richter
"""

import SVMLearner as svm
import learnerV2a as rll

class Learner:
    
    def __init__(self):
        self.svml = svm.Learner(w_size=1000,hybrid=True)
        self.rll_sys = rll.Learner(0.001, 0.5, 0.001, 1, 12)
    
    def predict(self,price1,price2,tstep = 0):
        pred = self.rll_sys.predict(price1,price2)
        #pred = self.svml.predict(price1,price2,rll_decision=pred)
        return pred#*(-1)