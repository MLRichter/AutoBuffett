from __future__ import print_function
import matplotlib.pylab as plt
import Layer1.NLSVC as svm
import Layer1.learnerV2a as l
import Layer1.RLLSVM as rlvm
#import Layer1.SVMLearner as svm
#import Layer1.RecurrentSVM as rsvm
#import Layer1.Poly_Learner as pl
#import Layer1.MLP_Learner as mlp
import numpy as np
from Layer2.AccountV2 import Account as acc

if __name__ == "__main__":
    #setup

    #receive info
    final_out = list()
    for j in range(1):
        for i in range(10):
            #print("Now in iteration: "+str(i),end='\r')
    
    
            #make up default values
            num_learner = 1
            learners = list()
    
            learner = l.Learner(0.1, 0.1, 0.001, 1, 23)
            learner.threshold = 2
            #learner = svm.Learner()
            #learner = rsvm.Learner(adaption=0.32,transactionCost=1.5)
            #learner = nlsvm.Learner()
            #learner = pl.Learner(j,200)
            #learner = mlp.Learner(layers=2,mode='returns',n_itr=3)
            #learner = rlvm.Learner()
            account = acc("EURUSD",1000,0,0,0,2000)
            val_watch = list()
            val_watch.append(account.total_account_value())
    
            #learner = l.Learner(0.02,0.3,1,0.95,10)
            #numbers = (np.sin(np.linspace(0, np.pi*8, 201))/3)+np.linspace(0,1,201)*0.5
            numbers = (np.sin(np.linspace(0, np.pi*8, 20001))/3)+0.5
            #numbers = (np.linspace(0,np.pi*8, 201))
            #numbers = np.multiply(np.sin(np.linspace(0,np.pi*8,201))+1,np.linspace(0,np.pi*8,201)*1.01)
            #numbers = np.sin(np.linspace(0, np.pi*4, 201))+1
            for i in range(len(numbers)):
                numbers[i]+=  np.random.normal(0,0.03,1)
            pnumbers = numbers[:20000]
            preds = list()
            #execution loop
            for i in range(1):
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
               # assert isinstance(prediction, float)
                preds.append(prediction)
    
            final_out.append(account.total_account_value())
        print("------------------------------------------------------------------")
        print("Iteration:"+str(j))
        print("Maximum was: "+str(np.amax(final_out))+" with recurrence: "+str(np.argmax(final_out)))
        print("Mean final profit: "+ str(np.mean(final_out)))
        print("With variance: " + str(np.std(final_out)**2))

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.plot(np.linspace(0, np.pi*8,20000), pnumbers)
    ax1.plot(np.linspace(0, np.pi*8,20000), preds)

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.plot(range(len(val_watch)),val_watch)
    plt.xlabel('time in price-updates')
    plt.ylabel('total account value')
    plt.axis('tight')
    plt.show()

