import data.control
from data.control import get_Kline_csv
from datetime import datetime as dat
get_Kline_csv("BTCUSDT",interval="1d",startin=dat(2020,9,10,00,1,1),endin=dat(2020,12,10,00,1,1))
