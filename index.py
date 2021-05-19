#%%
from __future__ import (absolute_import, division, print_function,unicode_literals)
import data.control as ctrl
from data.control import get_Kline_csv
from datetime import datetime as dat
import os
import sys
import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd
# ----------------------------------
class TestStrategy(bt.Strategy):
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30   # period for the slow moving average
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
        if not self.position:  # not in the market
            if self.crossoverprice > 0 and self.crossoversma > 0 :  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossoversma < 0  or self.crossoverprice < 0:  # in the market & cross to the downside
            self.close()

    
# ---------------------------
if __name__ == '__main__':
    datapath =ctrl.dirc
    data = btfeeds.GenericCSVData(
    dataname=get_Kline_csv(name="BTCUSDT",interval="15m"),

    fromdate=dat(2021, 1, 1),
    todate=dat.now(),

    nullvalue=0.0,

    dtformat=('%Y-%m-%d %H:%M:%S'),

    datetime=0,
    open=3,
    high=1,
    low=2,
    close=4,
    volume=5,
    openinterest=-1)
    # Create a Data Feed
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    cerebro.broker.setcash(100000)
    cerebro.adddata(data)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.broker.setcommission(commission=0.002)
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
# %%
