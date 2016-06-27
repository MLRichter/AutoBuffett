# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 17:49:54 2016

@author: Mats Richter

This is a completely random decision maker.
The system is used to evaluate the performance of actual learners in this
system.
"""

import numpy as np

class Learner:
    
    # @input    the inputs are actually the same as for the default rll-learner
    #           no input parameter is used by this system. They only sit here
    #           for making learners easiert exchangable
    def __init__(self, learn = 0, adaption = 0, transCost = 0,weightDecay = 0, m = 0, serialNumber = 0):
        return
    
    #@input     2 prices parameters are not recognized by the function and only
    #           exist for the sake of changing the learners easily
    #@return    a evenly distributed random number between -1 and 1.
    def predict(price1 = 0, price2 = 0, tstep = 0):
        return (np.random.rand()-0.5)*2        