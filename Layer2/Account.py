__author__ = 'matsrichter'

import FX_Position2 as FX_Position
import Position_Container
import numpy as np

class Account:

    # @input start_capital  starting capital of home-currency
    # @input symbol         trading symbol of the fx-index traded
    # @param max_val        maximum value of the account ever reached
    # @param positions      list of all current trading positions
    def __init__(self, symbol, start_capital,tstep ,short_price, long_price, stopploss, lever=1):
        self.capital = start_capital
        self.symbol = symbol
        self.positions = Position_Container.Position_Container(lever)
        self.currentPrice_long = short_price
        self.currentPrice_short = long_price
        self.tstep = tstep
        self.stoploss = stopploss
        self.maxVal = self.capital
        self.lever = lever

    # updates parameters in the system
    def update(self,price_short,price_long,tstep):
        self.currentPrice_long = price_long
        self.currentPrice_short = price_short
        self.tstep = tstep
        if(self.positions.pos_state == 'long'):
            self.positions.update(self.currentPrice_long,tstep)
        else:
            self.positions.update(self.currentPrice_short,tstep)
        val = self.total_account_value()
        if(val > self.maxVal):
            self.maxVal = val

    # cleans up the position container, closing all over or underachieving positions in the process
    # adds the money earned by selling the position back to the capital
    # @return integer value of the closed position.
    def check_stoploss(self):
        l1 = self.positions.length()
        self.capital += self.positions.check_stoploss(self.stoploss)
        return l1 - self.positions.length()

    #sells all open positions
    def sell_all(self):
        while(self.positions.length() > 0):
            self.capital += self.positions.pop()

    # failure state evaluator-function
    # @return the total value of the account in home currency.
    #           the value is the current with all summed up position profits
    def total_account_value(self):
        return self.positions.total_val() + self.capital


    def check_total_stoploss(self):
        if(np.fabs(self.positions.total_profit()) >= self.stoploss):
            self.sell_all()
            return True
        #trailing stoploss
       # if(np.fabs(self.maxVal - self.total_account_value()) >= self.stoploss):
       #     self.sell_all()
       #     return True
        return False

    # @input position  string: 'short' or 'long'
    # function executes orders from the risk managment system if a new position is taken or an old one has to be sold
    # the function only works if capital is available for investment or positions are sold (returning money to the
    # capital in the process)
    def execute(self, position, quantity = 1, transcost = 0):
        price = 0
        #set the price of the transaction
        for i in range(quantity):
            if(position == 'long'):
                price = self.currentPrice_long
            elif(position == 'short'):
                price = self.currentPrice_short
            else:
                print("Invalid position statement: "+position)
                return

            #if the list is empty or the current position matches the trade signal, a new fx-position object is created
            #else close the highest profit position and return money to capital
            if self.positions.isempty() or self.positions.pos_state == position:
                if(self.capital > price):
                    new_pos = FX_Position.FX_Position(self.symbol,position, price, self.tstep)
                    self.positions.insert(new_pos)
                    self.capital -= price
            else:
                self.capital += self.positions.pop()