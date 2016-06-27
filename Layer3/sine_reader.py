# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 14:21:59 2016

@author: saltking
"""

__author__ = 'matsrichter'
import numpy as np
import csv

#DUMMY READER FOR FOREX INDICES

class FX_Reader:
    #@input timested  time between ticks in seconds
    def __init__(self, time_step = 1):
        self.q = self.iterate()
        self.time_step = time_step
        self.tstep = 0
        self.data = (np.sin(np.linspace(0, np.pi*2, 20000))/10)+1
        #self.data += (np.cos(np.linspace(0, 50*np.pi*8, 20001))/3)+0.5
        self.data += (np.sin(np.linspace(0, np.pi*16, 20000))/100)

    def readPrice(self):
        if(self.time_step == 1):
            return self.q.next()
        else:
            for i in range(self.time_step-1):
                self.q.next()
            return self.q.next()

    def iterate(self):
        for j in range(10):
            for i in self.data:
                price = i + np.random.normal(0,0.001)
                yield (price, 1/price,str(len(self.data)*j))