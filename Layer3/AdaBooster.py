from __future__ import division
__author__ = 'matsrichter'
import Layer1.learnerV2a as l
import numpy as np

class AdaBooster:

    # AdaBooster, learn, adaption, transactinCost, weightDecay and m are required keys inside the instruction dict
    def __init__(self, instruction_dict):
        self.learners = list()
        for i in range(instruction_dict['AdaBoost']):
            self.learners.append(l.Learner(instruction_dict['learn'],instruction_dict['adaption'],
                                           instruction_dict['transactionCost'],instruction_dict['weightDecay'],
                                           instruction_dict['m']))
        self.weight = [1]*len(self.learners)
        self.tstep = 0
        self.profit = list()
        for i in range(len(self.learners)):
            self.profit.append(list())
        return

    # updates the parameters, for simplicity all learners use the same parameters
    # probably that will change in future version
    def update(self, instruction_dict):
        for i in range(instruction_dict['AdaBoost']):
            self.learners[i].learn = instruction_dict['learn']
            self.learners[i].adaption = instruction_dict['adaption']
            self.learners[i].transCost = instruction_dict['transactionCost']
            self.learners[i].weightDecay = instruction_dict['weightDecay']
        return

    # predicts via n RLL algorithm the course
    def predict(self,price1,price2):
        decision = 0
        for i in range(len(self.learners)):
            self.profit[i].append(self.learners[i].profit[0])
            if(len(self.profit[i]) > 3000):
                self.profit[i].pop(0)
            decision += self.learners[i].predict(price1,price2)*self.weight[i]
        if(self.tstep > 3000):
            self.updateWeight()
        self.tstep+= 1
        return np.tanh(decision)

    #function updates the weight vector by calculating the error rate and the information gain based on that error
    def updateWeight(self):
        for i in range(len(self.weight)):
            err = self.getError(i)
            log_err = (1-err)/err
            log_err = np.log2(log_err)
            self.weight[i] = 0.5*log_err
        return


    #get errors based on profit of a single learner
    #the data weight is implicitly defined by the inverse sum of all absolute profit/loss values
    def getError(self, index):
        losses_index = np.array(self.profit[index]) < 0
        print losses_index
        losses = np.fabs(np.sum(np.array(self.profit[index][np.array(losses_index)])))
        losses /= losses + np.sum(self.profit[index][np.array(self.profit)] >= 0)
        return losses



