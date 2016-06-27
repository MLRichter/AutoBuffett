# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 22:55:58 2016

Algorithm:

    1. call init by main
    2. call update every iteration, updating the list
    3. call eof_shutdown() to calculate the computational intensive stuff
       and print everything of interest

@author: Mats Richter
"""

import numpy as np
import matplotlib as plt
import csv as c

class Toolbox:

    def __init__(self,instruction_dict):
        #set starting values
        self.account_val_list = [instruction_dict['account_val']]
        self.date_list = list()
    
    #update self.parameters (primarily lists an not compute-intensive stuff)
    def update(self,instruction_dict,date = None, sharpe=False):    
        self.account_val_list.append(instruction_dict['account_val'])
#        self.account_cap_list.append(instruction_dict['account_val']-instruction_dict['capital'])
        self.date_list.append(instruction_dict['tstep'])
        return
        
    #save the profit graph as CSV 
    def save_csv(self,message,instruction_dict):
        f = open('stat_dump/'+message+'_'+instruction_dict['symbol']+".csv",'w')
        writer = c.writer(f,delimiter=' ')
#        writer2 = c.writer(self.csv_inv,delimiter=' ')
        for i in range(len(self.date_list)):    
            writer.writerow([self.date_list[i],self.account_val_list[i]])    
#           
        f.close()  
        return