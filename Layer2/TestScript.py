__author__ = 'matsrichter'

import Position_Container as pc
import Risk_Manager as rm
import FX_Position2 as fxp
import Account as acc
import AccountV2 as acc2
import matplotlib.pylab as plt
import numpy as np


testAccount = acc.Account("EUR/USD",101,0,1,1,0.2)
testAccount2 = acc2.Account("EUR/USD",101,0,1,1,0.2)

ac1 = list()
ac2 = list()

testAccount.stoploss, testAccount2.stoploss = 100,100

#testAccount.execute('long',100)
#testAccount2.execute('long',100)
ac1.append(testAccount.total_account_value())
ac2.append(testAccount2.total_account_value())
a = np.linspace(0,np.pi * 4,1000)
price = 0
changer = -1
for i in range(1):
    for i in range(1000):
        price = np.sin(a[i])
        testAccount.execute('long',1)
        testAccount2.execute('long',1)
        testAccount.update(price,price,i)
        testAccount2.update(price,price,i)   
        ac1.append(testAccount.total_account_value())
        ac2.append(testAccount2.total_account_value())

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.plot(range(len(ac1)),ac1)
ax1.plot(range(len(ac2)),ac2)
print(testAccount.capital)
print(testAccount2.capital)
print(ac1.pop())
print(ac2.pop())
    
    
    

