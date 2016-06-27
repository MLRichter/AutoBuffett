__author__ = 'matsrichter'

import urllib2
import time

class FX_Reader():

    #returns longPrice,shortPrice
    def readPrice(self):
        response = urllib2.urlopen('http://webrates.truefx.com/rates/connect.html?f=csv&c=EUR/USD')
        htmlLines = response.readlines()
        currencyInfo = htmlLines[0].split(",")
        offer = currencyInfo[4] + currencyInfo[5]
        
        longPrice, shortPrice = offer,offer
        return float(longPrice), 1/float(shortPrice)