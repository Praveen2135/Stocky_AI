from deta import Deta
import numpy as np
import pandas as pd

class StockyDb:
    def __init__(self):
        self.deta = Deta('d0p5if1f_GSnmoPk32YPhwKaJzN6sq7hM2DN4XPks')
        self.db = self.deta.Base('StockyAI')
        
    def save_to_DB(self,ticker,df):
        date_=[]
        open_=[]
        high_=[]
        low_=[]
        close_=[]
        for i in range (0,len(df)):
            df['Close']=df['Close'].astype(float)
            df['Low']=df['Low'].astype(float)
            df['High']=df['High'].astype(float)
            df['Open']=df['Open'].astype(float)
            date_.append(df['Date'][i])
            open_.append(df['Open'][i])
            high_.append(df['High'][i])
            low_.append(df['Low'][i])
            close_.append(df['Close'][i])
        self.db.put({'key':ticker,'date':date_,'open':open_,'high':high_,'low':low_,'close':close_})
    
    def ticker_df(self,ticker):
        return self.db.get(key=ticker)
    
    def get_all_ticker(self):
        tickers=[]
        for i in range(0,self.db.fetch().count):
            tickers.append(self.db.fetch().items[i]['key'])
        return tickers
    