# crypto-project-py-2021-ICT

## this project is an afort to build crypto trading bot - market screaner 
### pls contribute :)

## first step :
  ##### i built a data controller for fetch specified symbol and interval with selectable preiod that save as csv
  ##### libs: pandas datetime binance os
  ##### path: data/control.py/get_Kline_csv (func)
  ##### example:  get_Kline_csv("BTCUSDT",interval="1d",startin=dat(2020,9,10,00,1,1),endin=dat(2020,12,10,00,1,1))
  ##### output: is a csv file that contain date + ohlc + volume + noft (number of trade)
