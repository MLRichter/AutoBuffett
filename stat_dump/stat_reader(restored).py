# -*- coding: utf-8 -*-
"""
Created on Fri May 20 14:01:19 2016

@author: saltkind
"""

import re
import numpy as np

name = 'MAC_rSVM_exp(1)_final.txt'
f = open(name,'r')

prices = list()
pattern = re.compile('\d')
s = 'lel'
try:
    while(s != ''):
        s = f.readline()
        if(re.match(pattern,s)):
            line = re.split(' ', s)
            prices.append(float(line[1]))
           # print line[1]
        
except:
    f.close()
    print "EOF"
f.close()    

median = np.median(prices)
mu = np.mean(prices)
sigma= np.std(prices)
best = np.amax(prices)
worst = np.amin(prices)

print(median)
print(mu)
print(sigma)
print(best)
print(worst)

f = open(name,'a')
f.seek(0,2)
f.write('\nThis are the overall final results\n')
for i in range(50):
    f.write('#')
f.write('\n')
f.write("mu_profit: "+str(mu)+"\n")
f.write("sigma:     "+str(sigma)+'\n')
f.write('median:    '+str(median)+"\n")
f.write('best:      '+str(best)+"\n")
f.write('worst:     '+str(worst)+"\n")
f.close()


    
