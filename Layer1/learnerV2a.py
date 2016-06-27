__author__ = 'matsrichter'
import numpy as np
import random as rng

# everything with a time iterator needs to be a queue
#   find out what this M is all about and how many neurons are needed
#   debugging
#   cleanup

class Learner:
    #   Settings that worked fine
    #   please ote, that the second parameters is currently of no use and will therefore not affect the
    #   operations of this programm
    #   learner = l.Learner(0.65, 0.5, 0.001, 1, 10)
    def __init__(self, learn, adaption, transCost,weightDecay, m, serialNumber = 0):
        self.weightDecay = weightDecay
        self.m = m
        self.adaption = adaption                         #   adaption for the sharpeRatio
        self.transCost = transCost
        self.learn = learn
        self.tstep = 0                                   #   timestep with offset m
        self.learnerToggle = False
        self.serialNumber = serialNumber

        #   Data-storage-Lists
        #   all lists are in historical order
        self.returns = list()
        self.weights = np.ones(m + 2)
        for i in range(len(self.weights)):
            self.weights[i] *= rng.random()
        self.profit = np.zeros(2)
        self.prediction = np.zeros(2)                   #   [0] = F_t-1 [1] = F_t
        self.dFold = np.ones(m + 2)                     #   derivate-value of the prediction at point t-1
        self.dF = np.ones(m +2)                         #   derivate-value of the prediction at point t
        self.x = np.ones(m + 2)                         #   x-vector for multiplication with the weight vector

        #   stuff for the sharpe-ratio calculation
        self.sharpeA = 0
        self.sharpeB = 0
        self.oldSharpeA = 0
        self.oldSharpeB = 0

        #self debug
        self.devProfit = 0
        self.devPerf = 0
        self.dotProd = 0
        self.deltaW = 0
        self.profitCount = list()
        self.totalProfit = 0
        
        #threshold for weight decay
        self.threshold = 2

    #   function update the weight vector
    def updateWeight(self):
        self.deltaW = self.learn * self.getWChange()
        self.weights = self.weights*self.weightDecay + (self.learn * self.getWChange())

    #   returns the change in the weight vectors (without adjustmen by the learnparameter)
    def getWChange(self):
        solution = self.derivePerformance()
        partSol = np.dot(self.deriveProfitPrediction(self.tstep), self.dF)
        partSol += np.dot(self.deriveProfitPrediction(self.tstep - 1) , self.dFold)

        #print(solution)
        #print((self.deriveProfitPrediction(self.tstep - 1)))
        #print(self.deriveProfitPrediction(self.tstep))
        solution *= partSol
        return solution

    #   derivative with respect to the profit of the sharpe-ratio derived by the adaption parameter.
    #   this is a performance measurement for the learning algorithm
    def derivePerformance(self):
        self.devPerf = self.oldSharpeB - (self.oldSharpeA * self.profit[1])
        denom = ((self.oldSharpeB - (self.oldSharpeA ** 2)) ** (3 / 2))
        #in case denominator is zero        
#        if(denom == 0):    
#            return self.devPerf/0.0001
#        else:
        return self.devPerf/denom

    #   derivative of the Profit with respect to the prediction parameter. timestep of the prediction parameter
    #   is given by the parameter time
    #   @input  time timestep of the profit
    #   @return given the current timestep, the derivative with respect to F_t of the Profit (the current prediction)
    #           otherwise the function derives the function with respect to F_t-1 (the previous prediction)
    def deriveProfitPrediction(self, time):
        self.devProfit = 0
        if (self.prediction[1] < self.prediction[0]):
            self.devProfit = (-1) * self.transCost
        else:
            self.devProfit = self.transCost
        if (self.tstep == time):
            return self.devProfit
        else:
            return self.devProfit + self.returns[len(self.returns) - 1]

    def update_dF(self):
        self.dFold = self.dF
        self.dF = (1 - (self.prediction[1]**2)) * (self.x + (self.weights[self.m + 1] * self.dFold))
        return 0

    # Updates the parameters for sharpe ratio
    # the current values of sharpeA and B are shifted in oldSharpeA and B
    def updateSharpe(self):
        self.oldSharpeA = self.sharpeA
        self.oldSharpeB = self.sharpeB

        #   Alernative computation method
        if self.tstep < 3000:
            self.totalProfit += self.profit[1]
            self.sharpeA = np.mean(self.profitCount)
            self.sharpeB = np.std(self.profitCount)
        else:
            self.sharpeA = self.oldSharpeA + (self.adaption*(self.profit[1] - self.oldSharpeA))
            self.sharpeB = self.oldSharpeB + (self.adaption*((self.profit[1] ** 2) - self.oldSharpeB))

    #shifts the older profit at position[0] and adds a new up-to-date-profit-value at position [1]
    def updateProfit(self):
        newProfit = self.prediction[0]*self.returns[len(self.returns)-1]
        newProfit -= (self.transCost * np.fabs(self.prediction[1] - self.prediction[0]))
        self.profit[0] = self.profit[1]
        self.profit[1] = newProfit

    #   @input p1   the price at the point p(t-1)
    #   @input p2   the price at the point p(t)
    #   @return tanh(w.T * x_t) where x_t = [1, r_1,...,r_t-m, F_t-1] this is the approximation of a signum function
    #           1 stands for buying, -1 for selling and 0 for holding
    def predict(self, p1, p2):
        #   increase timestep
        self.tstep += 1
        #   append new return value to the historical data
        self.returns.append(p2 - p1)
        #sliding window adjustment
        if(len(self.returns) > 3000):
            self.returns.pop(0)
        #   prepare x-array
        for i in range(len(self.x)):
            if i == 0:
                continue
            elif i <= self.m and i != 0:
                #   handling if not enough data to feed the network
                if(0 < len(self.returns)-i):
                    self.x[i] = self.returns[len(self.returns) - i]
                else:
                    self.x[i] = 0
            else:
                self.x[i] = self.prediction[1]

        pred = np.tanh(np.dot(self.weights, self.x))
        self.dotProd = np.dot(self.weights, self.x)

        #shift older prediction into position[0] and add new primary position
        self.prediction[0] = self.prediction[1]
        self.prediction[1] = pred
        self.updateProfit()
        self.update_dF()

        # The system won't start learning until enough data is saved for calculating the init-values of the sharpe-ratio
        if(self.learnerToggle):
            self.updateSharpe()
            self.updateWeight()
        
        #normalize weights, if they get to large
        if(np.sum(self.weights) > self.threshold):
            self.weights *= 0.7
        #if self.tstep < self.m+1:
        self.profitCount.append(self.profit[1])
        # sliding window for profit count
        if(len(self.profitCount) > 3000):
            self.profitCount.pop(0)
        if self.tstep == self.m+1:
            self.sharpeA = np.mean(self.profitCount)
            self.sharpeB = np.std(self.profitCount)
            self.learnerToggle = True
        #recalc preduction with better weights
        self.prediction[1] = np.tanh(np.dot(self.weights, self.x))
        if(self.tstep >= 40000):
            return self.prediction[0] 
        else:
            return 0

    def stopLearning(self):
        self.learnerToggle = False

    def startLearning(self):
        self.learnerToggle = True

