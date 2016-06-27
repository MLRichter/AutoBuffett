__author__ = 'matsrichter'

import Communicator_Test as com
import Layer2.AccountV2 as acc
import Layer2.Risk_Manager as rm
import time as time
import numpy as np

class Layer2:

    def __init__(self,instruction_dict):
        symbol = instruction_dict['symbol']
        capital = instruction_dict['capital']
        self.account = acc.Account(symbol,capital,time.time(),0,0,instruction_dict['stoploss'],instruction_dict['lever'])
        self.capital_set = False
        self.symbol_set = False
        self.communicator = None
        self.risk_manager = rm.Risk_Manager(self.account,instruction_dict['risk_aversion'],instruction_dict['max_draw_down'])
        self.tstep = 0
        #history of the decisions for cheking "jumping" behaviour
        #self.jumpScore = 0
        #self.decision_history = list()
        self.block_score = False
        self.last_investments = list()
        self.last_investments.append(0)

    def adCom(self, communicator):
        assert(isinstance(communicator,com.Sender_Receiver))
        self.communicator = communicator
    
    #this function is build for debugging purposses and detects long times
    #of (peseudo)-inactivity by the system
    def block_detector(self, instruction_dict):
        #inv = self.account.positions
        #if(np.fabs(inv - np.sum(self.last_investments)) < 5 and self.tstep > 4000):
        #    print("block detected")
        #self.last_investments.append(inv)
        #if(len(self.last_investments) > 100):
        #    self.last_investments.pop(0)
        if(self.tstep%300 == 0):
            self.last_investments.append(self.account.total_account_value())
            self.block_score = True
        if(len(self.last_investments) > 3):
            self.last_investments.pop(0)
            
        if(self.tstep > 4000):
            if(np.fabs(self.last_investments[0]- self.last_investments[1]) < 0.1 and self.block_score and self.account.positions < 5):
#                print "BLOCK DETECTED"
                self.block_score = False
        return

    def call(self, instruction_dict):
        self.tstep += 1

        self.account.update(instruction_dict['short_price'],instruction_dict['long_price'],self.tstep )
        if('stoploss' in instruction_dict):
            self.account.stoploss = instruction_dict['stoploss']

        #update risk manager
        if('risk_aversion' in instruction_dict):
            self.risk_manager.risk_aversion = instruction_dict['risk_aversion']
        if('max_draw_down' in instruction_dict):
            self.risk_manager.max_draw_down = instruction_dict['max_draw_down']
        if('short_price' in instruction_dict)  and ('long_price' in instruction_dict):
            self.account.update(instruction_dict['short_price'],instruction_dict['long_price'],self.tstep)

        l1_decision = instruction_dict['decision']

        #check fatal error-state of finances
        #deactivated for testing purposses
        #if(self.risk_manager.isBroke):
        #    instruction_dict['ERROR'] = "isBroke"
        # TERMINATION FATAL ERROR STATE OF CODE REACHES THIS LINE

        #check for jumping behavior
        #self.decision_history.append(l1_decision)
        #if(len(self.decision_history) == 100):
        #    decision_div = np.zeros(99)
            #if the difference between two adjacent decisions is too high reset
            #the learner instantly
        #    for i in range(99):
        #        decision_div[i] = np.fabs(self.decision_history[i]-self.decision_history[i+1])
        #    if(np.mean(decision_div) >= 1.5 and not self.risk_manager.on_cooldown):
        #        instruction_dict['resetL'] = True
        #        self.risk_manager.set_cooldown(2000)
        #    self.decision_history = list()
                
        
        #evaluate risk and execute decision if needed
        if(self.risk_manager.eval_risk(l1_decision)):
            #print(l1_decision)
            if(instruction_dict['decision'] > 0):
                self.account.execute('long')
            elif(instruction_dict['decision'] < 0):
                self.account.execute('short')

        #send decision
        instruction_dict['account_val'] = self.account.total_account_value()
        instruction_dict['capital'] = self.account.capital

        #self.block_detector(instruction_dict)                
        
        self.communicator.send(instruction_dict,'l3')