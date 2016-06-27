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

#global variables
global best_acc_val
global worst_acc_val
#starting capital DO NOT CHANGE
global STARTING_CAPITAL
#shapré-ratio as performance measure
global sharpe_ratio
global account_val_list
global account_cap_list
global max_returns
global min_returns
global return_list
global date_list
#file pointers on the data-and the csv-file
global f
global csv

def init(instruction_dict):
    #best and worst total account value ever
    global best_acc_val
    global worst_acc_val
    global account_val_list
    #starting capital
    global STARTING_CAPITAL
    global sharpe_ratio
    global account_cap_list
    global return_list
    global date_list
    global f
    global csv
    #set starting values
    best_acc_val = instruction_dict['capital']
    worst_acc_val = instruction_dict['capital']
    STARTING_CAPITAL = best_acc_val
    account_val_list = [best_acc_val]
    account_cap_list = [best_acc_val]
    return_list = list()
    date_list = list()
    if(not 'f' in globals()):
        f = open('stat_dump/test'+instruction_dict['symbol']+".txt",'w+')
    if(not 'csv' in globals()):
        csv = open('stat_dump/test'+instruction_dict['symbol']+".csv",'wb')

#call in the end (after EOF-Error occured), calculates the systems sharpé ratio
#and other perofmrnace evalutation stuff
def eof_shutdown():
    global account_val_list
    global max_returns
    global min_returns
    global return_list    
    global best_acc_val
    global worst_acc_val    
        
    calc_sharpe()
    best_acc_val = np.amax(account_val_list)
    worst_acc_val = np.amin(account_val_list)
    max_returns = np.amax(return_list)
    min_returns = np.amin(return_list)
    return

#update global parameters (primarily lists an not compute-intensive stuff)
def update(instruction_dict,date = None, sharpe=False):
    global best_acc_val
    global worst_acc_val
    #starting capital DO NOT CHANGE
    global STARTING_CAPITAL
    #shapré-ratio as performance measure
    #global sharpe_ratio
    global account_val_list
    global account_cap_list
    global return_list
    global date_list

    account_val_list.append(instruction_dict['account_val'])
    account_cap_list.append(instruction_dict['capital'])
    date_list.append(instruction_dict['tstep'])
    return_list.append(account_val_list[len(account_val_list)-1]-account_val_list[len(account_val_list)-2])    
    return

#calculate the sharpé ratio   
def calc_sharpe():
    global return_list
    returns = np.array(return_list)
    global sharpe_ratio
    sharpe_ratio = np.mean(returns)/np.std(returns)
    return
    
def print_and_save(instruction_dict):
    #global variables
    global best_acc_val
    global worst_acc_val
    #starting capital DO NOT CHANGE
    global STARTING_CAPITAL
    #shapré-ratio as performance measure
    global sharpe_ratio
    global account_val_list
    global account_cap_list
    global max_returns
    global min_returns
    global return_list
    global f
    
    f.write('Iteration: '+str(instruction_dict['iteration'])+'\n')
    f.write('Insturction Dictionary'+str(instruction_dict)+'\n')
    f.write('Best Account Value: '+str(best_acc_val)+'\n')
    f.write('Worst Account Value: '+str(worst_acc_val)+'\n')
    f.write("END VAL: "+str(instruction_dict['account_val'])+'\n')
    f.write('\n')
    f.write('Starting Capital: '+str(STARTING_CAPITAL)+'\n')
    f.write('Sharpe Ratio: '+str(sharpe_ratio)+'\n')
    f.write('\n')
    #f.write(str(account_val_list)+'\n')
    #f.write(str(account_cap_list)+'\n')
    f.write('Best Return: '+str(max_returns)+'\n')
    f.write('Worst Return: '+str(min_returns)+'\n')
    #f.write(str(return_list)+'\n')
    f.write("\n")
    f.write('\n')
    f.write('\n')
    #f.close()
    save_csv()
    return
    
#save the profit graph as CSV 
def save_csv():
    global acount_val_list
    global date_list 
    writer = c.writer(csv,delimiter=' ')
    for i in range(len(date_list)):    
        writer.writerow([date_list[i],account_val_list[i]])    
    return
    
def print_special(message):
    global f
    f.write(message)
    f.write('\n')

def final_shutdown():
    global f
    global csv
    f.close()
    csv.close()
    return