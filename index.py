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
import requests as req
import time
from analisys.control import TestStrategy
from notfication.control import notfication
# ----------------------------------
bot = notfication()
        

# ---------------------------
if __name__ == '__main__':
    datapath =ctrl.dirc
    data = btfeeds.GenericCSVData(
    dataname=get_Kline_csv(name="BTCUSDT",interval="1h"),

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
