# -*- coding: utf-8 -*-
"""
Created on Sun May  8 10:43:04 2016

This thing reads and plots csv_files provided in the source code.
Made to get pretty graphs for the bachelor thesis :3

@author: Mats Leon Richter
"""


import matplotlib.pyplot as mpl
import csv

global f_name

def read():
    global f_name
    with open(f_name,'rb') as f:
            reader = csv.reader(f)
            tstep = 0
            for row in reader:
                proto = row[0]
                date, val= proto.split(' ')
                yield (date,float(val))

#name_list = ['testsine_mlp(1).csv','testsine_naiveSVM(2).csv','testsine_RLL(1).csv',
#             'testsine_nlSVM(1).csv','testsine_rSVM(1).csv','testsine_poly(1).csv','testsine_rng(1).csv','testsine_bh+(1).csv','testsine_bh-(1).csv']
#axis_labels = ['MLP','Naive SVM','Recurrent NN', 'Nonlinear SVM', 'Recurrent SVM','Polynomialregressor','RandomTrader','Buyer','Seller']
name_list = ['worst_nSVM_exp(2).csv','best_RNG_testlauf_exp(1).csv','best_BH+_testlauf_exp(1).csv']
axis_labels = ['Naive SVM','Random Trader','Buyer']
for i in range(len(name_list)):
    f_name = name_list[i]
    label_name = axis_labels[i]
    liste = list()
    dates = list()
    q = read()
    tstep = 0
    while(True):
       #print(reader.readPrice())
        try:
            tmp = q.next()
            d = tmp[0]
            p = tmp[1]
            tstep += 1
            if(tstep%1000 == 0):
                liste.append(p)
                dates.append(d)
        except:
            break
    date_len = len(dates)
    size = len(dates)/10
    label = list()
    for j in range(0,len(dates),size):
        label.append(dates[j])
    mpl.xticks(range(0,len(dates),size),label,rotation=45)
    mpl.grid(True)
    #mpl.ylim((0,1.5))
    mpl.xlabel("Zeit")
    mpl.ylabel("Preis")
   # if i >= len(name_list)-3:
    #    mpl.plot(range(len(dates)),liste,'--',label=label_name)
   # else:
    mpl.plot(range(len(dates)),liste,'-',label=label_name)        
mpl.legend(loc='upper left')
mpl.show()


    