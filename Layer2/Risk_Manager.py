__author__ = 'matsrichter'

import numpy as np
import AccountV2 as acc
import time

class Risk_Manager:

    # @param isBroke failure state. System has fatal error and stops functioning if this is True
    def __init__(self, account, risk_aversion_factor, max_draw_down):
        assert(isinstance(account, acc.Account))
        self.account = account
        self.cooldown = 40000
        self.tstep = 0
        self.isBroke = False
        self.risk_aversion = risk_aversion_factor
        self.max_draw_down = max_draw_down
        self.max_profit = 0

    #evaluates risk of a trade
    #   @input decision:    float: the raw decision
    def eval_risk(self,decision):
        self.tstep += 1
        #close stoplosses
        loss = self.account.check_stoploss()
        #loss = False
        #set cooldown if stoplosses were surpassed
        if(loss):
           self.set_cooldown()
           return False
        #if(self.account.check_total_stoploss()):
        #    self.set_cooldown()
        #    return False
        #if currently on cooldown, no trade is performed
        if(self.on_cooldown()):
            return False
        if(self.risk_aversion > np.fabs(decision)):
            return False
        if(self.account.maxVal - self.account.total_account_value() > self.max_draw_down):
            self.isBroke = True
            self.account.sell_all()
            return False
        return True


    # sets the cooldown (in seconds) indicated by length if not already set
    # while cooldown >= tstep no trading decision of the learner is processed
    # however, stoploss is still performed if nessasry
    # @input cooldown time in seconds
    def set_cooldown(self, length = 100):
        if(self.tstep > self.cooldown):
            self.cooldown = self.tstep + length
            return
        else:
            return

    def sell_all(self):
        self.account.sell_all()

    def on_cooldown(self):
        return self.cooldown > self.tstep
