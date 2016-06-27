# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 23:08:55 2016

@author: saltking
"""

__author__ = 'matsrichter'
import numpy as np
import csv

#DUMMY READER FOR FOREX INDICES

class FX_Reader:
    #@input timested  time between ticks in seconds
    def __init__(self, time_step = 1,pre=False):
        self.q = self.iterate()
        self.time_step = time_step
        self.tstep = 0
        self.pre = pre

    def readPrice(self):
        if(self.time_step == 1):
            return self.q.next()
        else:
            for i in range(self.time_step-1):
                self.q.next()
            return self.q.next()

    def iterate(self):
        with open('Final.csv','rb') as f:
            reader = csv.reader(f)
            tstep = 0
            for row in reader:
                #print(row)
                tstep += 1
                #if(tstep%2 == 0):
                #Error detection in data
                p1 = float(row[2])
                if(p1 > 2 or p1 < 0):
                    continue
                p2 = 1/p1
                if(not self.pre):
                    yield (p1, p2,str(row[0]))
                else:
                    yield (p1,p2)