__author__ = 'matsrichter'

import FX_Position2 as FX_Position
import Position_Container
__author__ = 'matsrichter'

import FX_Position2 as FX_Position
import Position_Container
import numpy as np

class Account:

    # @input start_capital  starting capital of home-currency
    # @input symbol         trading symbol of the fx-index traded
    # @param max_val        maximum value of the account ever reached
    # @param positions      list of all current trading positions
    def __init__(self, symbol = '', start_capital = 1000,tstep = 0 ,short_price = 0, long_price = 0, stopploss = 50, lever=1):
        self.capital = start_capital
        self.symbol = symbol
        #counts the current open positions
        self.positions = 0
        self.old_price_short = 1
        self.old_price_long = 1
        self.currentPrice_long = short_price
        self.currentPrice_short = long_price
        self.state = 'undef'
        self.tstep = tstep
        self.stoploss = stopploss
        self.maxVal = self.capital
        self.best_price = 0
        #lever functionality not yet implemented
        self.lever = lever
        self.index = 0
    # updates parameters in the system
    def update(self,price_short,price_long,tstep = 0):
        self.index += 1
        before = self.total_account_value()        
        
        self.old_price_long = self.currentPrice_long
        self.old_price_short = self.currentPrice_short
        
        self.currentPrice_long = price_long
        self.currentPrice_short = price_short
        
        self.tstep = tstep
        val = self.total_account_value()
        if(val > self.maxVal):
            self.maxVal = val
        if(self.state == 'long'):
            price = price_long
        elif(self.state == 'short'):
            price = price_short
        else:
            price = 0
        #best price in lifetime of a position
        if(price > self.best_price):
            self.best_price = price
        #Error detector for unusual price-points
        #currently only used for checking the benchmark for errors
#        if(np.fabs(self.total_account_value() - before) >= 10):
#            print("Unusual behavior detected!")
            

    # cleans up the position container, closing all over or underachieving positions in the process
    # adds the money earned by selling the position back to the capital
    # @return integer value of the closed position.
    # if the latest price is the best price, we need to use the change from
    # the t-1 to t
    def check_stoploss(self):
        #if not positions are open, stoploss is unreachable
        if(self.positions == 0 or self.state == 'undef'):
            return False
        #select correct prices for current position-state
        if(self.state == 'long'):
            price = self.currentPrice_long
            old = self.old_price_long
        elif(self.state == 'short'):
            price = self.currentPrice_short
            old = self.old_price_short
        else:
            return False
        
        #if the current price is NOT the best price ever reached
        #we look for the divergence in basis points 
        if(price != self.best_price):
            ratio = price/self.best_price
        #if the price is the best price ever reached in position lifetime
        #measure difference between it and the previous
        else:
            ratio = price/old
        #figure out the basis point difference
        if(ratio > 1):
            ratio -= 1
        else:
            ratio = 1 - ratio
        #stoploss is reached iff the ratio differs
        #over oder undershoots a theshold of basis points
        if(ratio*10000 >= self.stoploss):
            self.sell_all()
            return True
        return False

    #sells all open positions
    def sell_all(self):
        if self.state == 'undef' or self.positions == 0:
            return
        if self.state == 'short':
            self.execute('long',self.positions)
        elif(self.state == 'long'):
            self.execute('short',self.positions)            
        return

    # failure state evaluator-function
    # @return the total value of the account in home currency.
    #           the value is the current with all summed up position profits
    def total_account_value(self):
        if(self.state == 'long'):
            price = self.currentPrice_long
        elif(self.state == 'short'):
            price = self.currentPrice_short
        else:
            return self.capital
        return self.capital+(self.positions * price)

    # @input position  string: 'short' or 'long'
    # function executes orders from the risk managment system if a new position is taken or an old one has to be sold
    # the function only works if capital is available for investment or positions are sold (returning money to the
    # capital in the process)
    def execute(self, position, quantity = 1, transcost = 0):
        #only positive quantities can be executed errorlessly
        if(quantity < 0):
            print("Error Negative Quantity: "+str(quantity))
            return
        #buy if no position is open or the order equals
        #the curren position hold
        if (position == self.state or self.state == 'undef'):
            self.state = position
            #if position is a long
            if(self.state == 'long'):
                #act only if enough money is left to do so
                if self.capital >= self.currentPrice_long*quantity:
                    #add newly opened positions
                    self.positions += quantity
                    #subtract the cost from the capital
                    self.capital -= self.currentPrice_long * quantity
                    #update best price
                    if(self.best_price < self.currentPrice_long):                
                        self.best_price = self.currentPrice_long
            #same handling for a 'short'position
            elif(self.state == 'short'):
                #act only if enough money is left to do so
                if self.capital >= self.currentPrice_short*quantity:
                    #add newly opened positions
                    self.positions += quantity
                    #subtract the cost from the capital
                    self.capital -= self.currentPrice_short * quantity
                    #update best price
                    if(self.best_price < self.currentPrice_short):                
                        self.best_price = self.currentPrice_short
            return
        #if current position is unequal to the current position hold
        #this is interpreted as a selling order
        else:
            #sell only what we have and oppen opposing position
            if(self.positions < quantity):
                quantity = self.positions
            #sell the quantity of positions for the given price
            if(self.state == 'long'):
                self.capital += self.currentPrice_long * quantity
            elif(self.state == 'short'):
                self.capital += self.currentPrice_short * quantity
            #remove sold positions
            self.positions -= quantity  
            #if no positions are hold, the state is now undefined              
            if(self.positions == 0):
                self.state = 'undef'
                self.best_price = 0
            return