
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
        treshold=0,
        preClose=0,
        dayinpos=0
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.atrs=bt.ind.ATR(period=self.p.pslow)
        self.atrf=bt.ind.ATR(period=self.p.pfast)
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.hlrange=self.data.high-self.data.low
        self.crossoversma = bt.ind.CrossOver(sma1, sma2)  # crossover signal
        self.crossoverprice = bt.ind.CrossOver(self.data.close,sma2) 
        #  # crossover signal
    def next(self):
        # Simply log the closing price of the series from the reference
        if(self.p.preClose): 
            if (self.datas[0].close>self.p.preClose):  # not in the market  # if fast crosses slow to the upside
                self.p.treshold+=1
                self.p.preClose=self.datas[0].close     
            elif(self.datas[0].close<self.p.preClose):    
                self.p.treshold-=1 
                self.p.preClose=self.datas[0].close    
            print(f" th is  {self.p.treshold} and {self.data.close} and {self.p.preClose }and {self.p.dayinpos} \n ")
            if (not self.position):
                if (self.p.treshold == 3) :
                    #bot.sendMessage(text="buy BTCUSDT"+self.datas[0].datetime.date(0).isoformat() +"price ->"+str( self.datas[0].close[0]))
                    self.buy()  # enter long
                    self.p.treshold=0
                    print(f"buy ")
            
            elif (self.p.treshold<-2 or self.p.dayinpos > 100 ):
                    self.p.treshold=0
                    self.p.dayinpos=0
                    self.close()
                    print(f"close buy ")
            
                    # bot.sendMessage(text="close BTCUSDT"+self.datas[0].datetime.date(0).isoformat() +"price ->"+str( self.datas[0].close[0]))
            else:
                self.p.dayinpos+=1        
        else: 
            self.p.preClose=1 

                    
           