__author__ = 'matsrichter'

import Layer1.learnerV2a as learner
import Layer1.RNJesus as learner2
import Layer1.SVMLearner as learner3
import Layer1.RecurrentSVM as learner4
import Layer1.RLLSVM as learner5
import Layer1.BuyAndHolder as learner6
import Layer1.NLSVC as learner7
import Layer1.Poly_Learner as learner8
import Layer1.MLP_Classifier as learner9

from Layer2.AccountV2 import Account
from Layer3.benchmark_reader import FX_Reader

import Layer3.AdaBooster as ab
import math
import Communicator_Test as com


class Layer1:

    def __init__(self,instruction_dict, communicator = None):
        self.learner_num = instruction_dict['learner']        
        self.num = 10
        if(self.learner_num == 9):
            self.num = 1
        #list of learners
        self.learners = list()  
        #list of accounts
        self.accounts = list()
        #active learner
        self.active = 0
        #reset_counter
        self.reset_c = 0
        
        self.communicator = communicator
        self.boosted = False
        
        #cycle measurements
        self.epoch_counter = 0
        self.batch_counter = 0
        self.batch_size = 4000
        
        for i in range(self.num):
            self.accounts.append(Account())
        
        if(instruction_dict['AdaBoost'] == 0):
            for i in range(self.num):
                if(instruction_dict['learner'] == 1):
                    trading_sys = learner.Learner(instruction_dict['learn'],instruction_dict['adaption'],
                                                       instruction_dict['transactionCost'],instruction_dict['weightDecay'],
                                                       instruction_dict['m'])
                elif(instruction_dict['learner'] == 2):
                    trading_sys = learner2.Learner()
                elif(instruction_dict['learner'] == 3):
                    trading_sys = learner3.Learner(recurrence=instruction_dict['m'],w_size=instruction_dict['w_size'])
                elif(instruction_dict['learner'] == 4):
                   #self,adaption = 0.5,transactionCost = 0.001, recurrence=35, realy_recurrent=False, w_size=20,label_par='r'):
                    #self.trading_sys = learner4.Learner(0.0001)
                    trading_sys = learner4.Learner(adaption=instruction_dict['adaption'],transactionCost=instruction_dict['transactionCost'],recurrence=instruction_dict['m'],w_size=instruction_dict['w_size'])
                elif(instruction_dict['learner'] == 5):
                    trading_sys = learner5.Learner()
                elif(instruction_dict['learner'] == 6):
                    trading_sys = learner6.Learner()
                elif(instruction_dict['learner'] == 7):
                    trading_sys = learner7.Learner(w_size=instruction_dict['w_size'])
                elif(instruction_dict['learner'] == 8):
                    trading_sys = learner8.Learner(degree=instruction_dict['poly'],epoch=instruction_dict['epoch'])
                elif(instruction_dict['learner'] == 9):
                            trading_sys = learner9.Learner(w_size=instruction_dict['w_size'],input_size=instruction_dict['m'],
                                                                layers=instruction_dict['layers'],adaption=instruction_dict['adaption'])
                #self.pre_train(trading_sys)                                                       
                self.learners.append(trading_sys)
                                                            
        self.price2 = 0
        self.price1 = 0

    def adCom(self, communicator):
        assert(isinstance(communicator,com.Sender_Receiver))
        self.communicator = communicator
        
    def reset_learner(self,instruction_dict, index):
        trading_sys = None
        if(instruction_dict['learner'] == 1):
            trading_sys = learner.Learner(instruction_dict['learn'],instruction_dict['adaption'],
                                          instruction_dict['transactionCost'],instruction_dict['weightDecay'],instruction_dict['m'])
        elif(instruction_dict['learner'] == 2):
            trading_sys = learner2.Learner()
        elif(instruction_dict['learner'] == 3):
            trading_sys = learner3.Learner(recurrence=instruction_dict['m'],w_size=instruction_dict['w_size'])
        elif(instruction_dict['learner'] == 4):
            trading_sys = learner4.Learner(adaption=instruction_dict['adaption'],transactionCost=instruction_dict['transactionCost'],recurrence=instruction_dict['m'],w_size=instruction_dict['w_size'])
        elif(instruction_dict['learner'] == 5):
            trading_sys = learner5.Learner()
        elif(instruction_dict['learner'] == 6):
            trading_sys = learner6.Learner()
        elif(instruction_dict['learner'] == 7):
            trading_sys = learner7.Learner(w_size=instruction_dict['w_size'])
        elif(instruction_dict['learner'] == 8):
            trading_sys = learner8.Learner()
        elif(instruction_dict['learner'] == 9):
            trading_sys = learner9.Learner(w_size=instruction_dict['w_size'],input_size=instruction_dict['m'],
                                           layers=instruction_dict['layers'],adaption=instruction_dict['adaption'])
        #self.pre_train(trading_sys)                                 
        self.learners[index] = trading_sys
        self.accounts[index].sell_all()
        self.accounts[index].capital = 1000
        return
    #train a learner    
    def pre_train(self,learner):
        reader = FX_Reader(pre=True)
        print("starting pre-training")
        try:
            while(True):
                tmp = reader.readPrice()
                learner.predict(tmp[0],tmp[1])
        except:
            print("pre training done")
            return
        return
        
    def eval_best(self,instruction_dict):
        best = 0
        index = 0
        for i in range(len(self.accounts)):
            if(best < self.accounts[i].total_account_value()):
                best = self.accounts[i].total_account_value()
                index = i
        if(best < 1000):
            index = -1
        #reset learner
        #print(self.batch_counter)
        if(index != self.batch_counter and self.reset_c == self.batch_counter):
            self.reset_learner(instruction_dict,self.batch_counter)
        #increment batch
        self.batch_counter += 1
        if(self.batch_counter >= self.num):
            self.batch_counter = 0 
        return index

    def call(self, instruction_dict):
        if 'ERROR' in instruction_dict:
            return 0
            
        if('resetL' in instruction_dict):
            if(instruction_dict['resetL']):
                self.reset_learner(instruction_dict,self.active)
                instruction_dict['resetL'] = False

        self.price2 = self.price1
        self.price1 = instruction_dict['long_price']
        for acc in self.accounts:
            acc.update(instruction_dict['short_price'],instruction_dict['long_price'])
        for trading_sys in self.learners:
            if(instruction_dict['learner'] == 1):
                trading_sys.adaption = instruction_dict['adaption']
                trading_sys.learn = instruction_dict['learn']
                trading_sys.transCost = instruction_dict['transactionCost']
                trading_sys.weightDecay = instruction_dict['weightDecay']
            elif (instruction_dict['learner'] == 4):
                trading_sys.adaption = instruction_dict['adaption']
                trading_sys.transactionCost = instruction_dict['transactionCost']
            elif (instruction_dict['learner'] == 9):
                trading_sys.adaption = instruction_dict['adaption']
        prediction = 0
        for i in range(len(self.learners)):
            #execute decisions on virtual accounts for performance measure
            decision = self.learners[i].predict(self.price1,self.price2)
            if(decision > 0):            
                self.accounts[i].execute('long')
            elif(decision < 0):
                self.accounts[i].execute('short')
                
            if(i == self.active):
                prediction = decision

        #prediction = self.learners[self.active].predict(self.price1,self.price2)
        #reset learner if prediction illegal
        if(math.isnan(prediction)):
            self.reset_learner(instruction_dict,self.active)
            prediction = 0
            
                                                   
        instruction_dict['decision'] = prediction
        self.epoch_counter += 1
        #after each batch, eval new, best learner
        if(self.epoch_counter%self.batch_size == 0 and self.learner_num != 9):
            self.active = self.eval_best(instruction_dict)
#            for acc in self.accounts:
#                acc.sell_all()
#                acc.capital = 1000
        if(self.epoch_counter >= self.batch_size*self.num and self.learner_num != 9):
            #after end of epoch, reset all accounts
            for acc in self.accounts:
                acc.sell_all()
                acc.capital = 1000
            self.epoch_counter = 0
            self.reset_c += 1
            if(self.reset_c >= self.num):
                self.reset_c = 1
        self.communicator.send(instruction_dict,'l2')