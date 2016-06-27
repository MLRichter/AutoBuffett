# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 07:02:04 2016

Yet another Benchmarking AI
This 'AI' basically sticks to a single position from start to finish
It executes this single option every time step with maximum confidence


@author: Mats Richter
"""

class Learner:
    
    def __init__(self,position=1):
        self.position = position
    
    def predict(self,new_price,old_price,tstep = 0):
        if(self.position == -1):
            return -1
        else:
            return 1