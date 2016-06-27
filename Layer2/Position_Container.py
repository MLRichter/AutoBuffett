__author__ = 'matsrichter'

import FX_Position2 as fxp
import numpy as np

class Position_Container:
    
    # @param poslist    list of positions
    def __init__(self, lever = 1):
        self.poslist = list()
        self.pos_state = 'undef'
        self.lever = lever
    
    #inserts a single FX_Position
    def insert(self, position):
        if self.isempty():
            self.pos_state = position.position
        self.poslist.append(position)
        self.sort()
    
    #closes the most profitable position of the specified type
    # @return   the profit of the closed position
    def pop(self):
        self.sort()
        pos = self.poslist.pop(len(self.poslist)-1)
        if(self.isempty()):
            self.pos_state = 'undef'
        return pos.sell_price + pos.get_profit(self.lever-1)

    def isempty(self):
        return len(self.poslist) == 0

    def length(self):
        return len(self.poslist)
    
    # sorts the positions by profit
    def sort(self):
        for i in range(len(self.poslist)):
            for j in range(len(self.poslist)-1-i):
                if(self.poslist[j].profit > self.poslist[j+1].profit):
                        self.poslist[j],self.poslist[j+1] = self.poslist[j+1],self.poslist[j]

    # @input the stoploss
    # this function cleans up all exsisting positions and sells all positions with to much loss/profit
    def check_stoploss(self, stoploss):
        total_stoploss_returns = 0
        while(len(self.poslist) > 0):
            if(not self.check_single_stoploss(stoploss)):
                break
            pos = self.poslist.pop(0)
            total_stoploss_returns += pos.sell_price
        return total_stoploss_returns

    #checks if the topmost position diverged at least stoploss-basis points
    def check_single_stoploss(self,stoploss):
        precent_stoploss = float(stoploss) / float(10000)
        if(self.poslist[0].old_best_change != 0):
            percent_change = self.poslist[0].old_best_change
        else:
            percent_change  = (self.poslist[0].best_price / self.poslist[0].sell_price)
        
        if(percent_change > 1):
            percent_change -= 1.0
        if(percent_change >= precent_stoploss):
            return True
        else:
            return False



    # @return the total profit of all positions
    def total_profit(self):
        total_profit = 0
        for i in self.poslist:
            total_profit += i.get_profit(self.lever)
        return total_profit

    def total_val(self):
        total_value = 0
        for i in self.poslist:
            total_value += i.get_sell_price() + i.get_profit(self.lever-1)
        return total_value

    # updates all FX_Position
    def update(self,price,time):
        for i in self.poslist:
            i.update(price,time)
        self.sort()
