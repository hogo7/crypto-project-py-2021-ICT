# _______library
#%%
import pandas as pd 
from binance.client import Client
import confuse
from datetime import datetime as dat
import datetime as dt
import os
import pathlib as path
import json
##TODO make config file

#%%
f = open ('config.json', "r")
conf = json.load(f)["config"]
mainPath=conf["app"]["path"]
# %% 
##TODO make conncetion file
api_key=conf["credit"]["API_KEY"]
key=conf["credit"]["API_SECRET"]
client = Client(api_key,key,{"timeout": 2000})
status = client.get_system_status()
print(status)
# %%
conf["app"]["path"]
# %% get data o f sepecifc symbole at any inteval any date scope
def get_Kline_csv(name,interval="1h",startin=dat(2020,1,1,00,1,1),endin=dat.now()):
        start=startin.strftime("%d %m,%Y")
        startff=startin.strftime("%d%m%Y")
        endff=endin.strftime("%d%m%Y")
        end=endin.strftime("%d %m,%Y")
        dirc=mainPath+"/data/csvs/"+name+"/"+interval
        filename="data"
        fileformat=".csv"
        ##info = client.get_symbol_info(name) ## check for is trading or not !
        print("from  "+start+" ->     "+end)
    ##get_historical_klines(symbol, interval, start_str, end_str=None, limit=500)
        flag=1
        while flag==1:
            try:
                data=client.get_historical_klines(name,interval,start,end)
                flag=0
            except:
                print("check your connection - ctrl-c for exit - we are retrying")
        print("date resived!!!")
        for x in range(len(data)):
            data[x][0]=dat.strptime(dat.fromtimestamp(int(data[x][0])/1000).strftime('%Y-%m-%d %H:%M:%S'),"%Y-%m-%d %H:%M:%S")
            for xx in range(1,len(data[0])-1):
                data[x][xx]=float(data[x][xx])
        dfdata=[]
        for x in range(len(data)):
            themplis=[]
            for xx in range(0,len(data[0])-1):
                if(xx<=5 or xx==8):
                    themplis.append(data[x][xx])
            dfdata.append(themplis)

        if not os.path.exists(dirc):
            os.makedirs(dirc)
            print("path successfuly created")
        else:
            print("folder found ")
        ## noft -> number of trades
        address=dirc+"/"+filename+fileformat 
        df=pd.DataFrame(columns=["date","open","high","low","close","volume","noft"],data=dfdata)
        df.set_index("date",drop=True,inplace=True)
        df.to_csv(address,mode="w")
        print("successfuly created")
        return address
# %%this function use to update chart symbols and last price of them 
# a=get_Kline_csv("ADAUSDT")
# name="amir"
# interval="1d"
# a=mainPath+"/data/csvs/"+name+"/"+interval
a=get_Kline_csv(name="ADAUSDT")
a
# %%this function use to update chart symbols and last price of them 
def update_Main_Chart():
    info=client.get_all_tickers()
    name="latest-chart"
    symdf=pd.DataFrame(columns=["symbol","price"],data=info)
    if not os.path.exists('./csvs/'+name+'/'):
        os.makedirs('./csvs/'+name+"/")
        print("path successfuly created")
    else:
        print("folder found ")

    symdf.to_csv("./csvs/"+name+"/mainChart.csv",mode="w",index=True)
    return "./csvs/"+name+"/mainChart.csv"
# %%
def get_all_hisData(interval="1d",startin=dat(2020,1,1,00,1,1),endin=dat.now()):
    address = update_Main_Chart() 
    df =pd.read_csv(address)
    addressBook=[]
    for x in range(0,df.size-1):
        tempdata={}
        symbol=df["symbol"][x]
        interval="1d"
        symdata=get_Kline_csv(symbol,interval=interval,startin=startin,endin=dat.now())
        tempdata={"symbol":symbol,"address":symdata,"start":startin.strftime("%Y-%m-%d %H:%M:%S"),"end":endin.strftime("%Y-%m-%d %H:%M:%S")}
        addressBook.append(tempdata)
    return addressBook
# %% 
# %% 
# def test area
##get_Kline_csv("BTCUSDT",interval="1d",startin=dat(2020,9,10,00,1,1),endin=dat(2020,12,10,00,1,1))

# %%data sample
'''kline sample
    { 0  1499040000000,      # Open time 
        #1  "0.01634790",       # Open
        #2 "0.80000000",       # High
        #3   "0.01575800",       # Low
        #4   "0.01577100",       # Close
        #5   "148976.11427815",  # Volume
        #6   1499644799999,      # Close time
        #7   "2434.19055334",    # Quote asset volume
        #8   308,                # Number of trades
        #   "1756.87402397",    # Taker buy base asset volume
        #   "28.46694368",      # Taker buy quote asset volume
        #   "17928899.62484339" # Can be ignored }
'''
        

