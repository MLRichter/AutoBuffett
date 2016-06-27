# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 11:56:23 2016

Regressive Support-Vecotor-Mashine

@author: saltking
"""

import sklearn.svm.SVR as sk
import numpy as np

class Learner:
    
    def __init__(self,instruction_dict):
        self.learner = sk()
        self.data = data
        return