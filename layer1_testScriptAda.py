from __future__ import print_function
import matplotlib.pylab as plt
__author__ = 'matsrichter'

import learnerV2a as l
import numpy as np
import Layer2.Account as acc
import Layer3.AdaBooster as ab

if __name__ == "__main__":
    #setup

    #receive info
    final_out = list()

    for i in range(1):


        #make up default values
        num_learner = 1
        learners = list()

        learner = l.Learner(0.65, 0.5, 0.001, 1, 10)
        account = acc.Account("EURUSD",1000,0,0,0,2000)
        val_watch = list()
        val_watch.append(account.total_account_value())

        #learner = l.Learner(0.02,0.3,1,0.95,10)
        #numbers = (np.sin(np.linspace(0, np.pi*8, 201))/3)+np.linspace(0,1,201)*0.5
        numbers = (np.sin(np.linspace(0, np.pi*8, 201))/3)+0.5
        #numbers = (np.linspace(0,np.pi*8, 201))
        #numbers = np.multiply(np.sin(np.linspace(0,np.pi*8,201))+1,np.linspace(0,np.pi*8,201)*1.01)
        #numbers = np.sin(np.linspace(0, np.pi*4, 201))+1
        for i in range(len(numbers)):
            numbers[i]+=  np.random.normal(0,0.03,1)
        pnumbers = numbers[:200]
        preds = list()
        #execution loop
        for i in range(40):
            for i in range(len(numbers)-1):
                learner.predict(numbers[i],numbers[i+1])

        #learner.stopLearning()

        for i in range(len(numbers)-1):
            account.update(1/numbers[i], numbers[i],i)
            prediction = learner.predict(numbers[i],numbers[i+1])
            val_watch.append(account.total_account_value())
            if(prediction < 0):
                account.execute('long')
            else:
                account.execute('short')
            assert isinstance(prediction, float)
            preds.append(prediction)

        final_out.append(account.total_account_value())

    print("Mean final profit: "+ str(np.mean(final_out)))
    print("With variante: " + str(np.std(final_out)**2))

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.plot(np.linspace(0, np.pi*8,200), pnumbers)
    ax1.plot(np.linspace(0, np.pi*8,200), preds)

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.plot(range(len(val_watch)),val_watch)
    plt.xlabel('time in price-updates')
    plt.ylabel('total account value')
    plt.axis('tight')
    plt.show()

