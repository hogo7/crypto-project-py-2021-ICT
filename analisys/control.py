
from __future__ import (absolute_import, division, print_function,unicode_literals)
import data.control as ctrl
from data.control import get_Kline_csv
from datetime import datetime as dat
import os
import sys
import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd
import requests as req
import time
from notfication.control import notfication
bot = notfication()
class TestStrategy(bt.Strategy):
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30,   # period for the slow moving average
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossoversma = bt.ind.CrossOver(sma1, sma2)  # crossover signal
        self.crossoverprice = bt.ind.CrossOver(self.data.close,sma2) #  # crossover signal
    def next(self):
        # Simply log the closing price of the series from the reference
        if (not self.position):
            if (self.crossoverprice < 0 and self.crossoversma < 0):  # not in the market  # if fast crosses slow to the upside
                self.buy()  # enter long
                bot.sendMessage(text="buy BTCUSDT"+self.datas[0].datetime.date(0).isoformat() +"price ->"+str( self.datas[0].close[0]))
            

            
        elif self.crossoverprice > 0 or self.crossoversma > 0 :
                self.close()
                bot.sendMessage(text="close BTCUSDT"+self.datas[0].datetime.date(0).isoformat() +"price ->"+str( self.datas[0].close[0]))
                
           