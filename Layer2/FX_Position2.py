__author__ = 'matsrichter'
import numpy as np

class FX_Position:

    # constructor creating a single FX position (buy / sell)
    # @input symbol     the trading symbol of the used index (String)
    # @input position   string describing the position
    #                   'short' = short position
    #                   'long' = long position
    # @input buy-price      the initial price of this position per unit
    # @param time     timestep of the trade or the last update
    #
    def __init__(self, symbol, position, buy_price, time):
        self.symbol = symbol
        self.buy_price = buy_price
        self.sell_price = buy_price
        self.best_price = buy_price
        self.old_best_change = 0
        self.profit = 0
        self.time = time
        self.position = position


    # @input current_price  the current price of the index
    def get_profit(self,lever=1):
        return self.profit * lever

    def get_sell_price(self):
        return self.sell_price

    def get_buy_price(self):
        return self.buy_price

    def get_symbol(self):
        return self.symbol

    def get_time(self):
        return self.time

    def update(self,new_price, time):
        self.sell_price = new_price
        self.profit = self.sell_price - self.buy_price
        if(self.best_price < new_price):
            #change if a new highes price was achieved, allowing the stoploss to kick in also in positiv changes
            self.old_best_change = new_price/self.best_price
            self.best_price = new_price
        else:
            self.old_best_change = 0
        self.time = time