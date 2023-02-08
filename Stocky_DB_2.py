#Importing all modules
from deta import Deta
import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
from yahoo_fin.stock_info import *
import time
import datetime as dt
import json
import requests

# this will be used to conect and do all functions related to DataBase
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
    
    def Recomodation(self):
        tickers = self.get_all_ticker()
        buy=[]
        sell = []
        
        for i in tickers:
            rec={}
            df=pd.DataFrame(self.ticker_df(i))
            H_max=df['high'].max()
            L_min=df['low'].min()
            H_date=(df[df['high']==H_max])['date'].to_list()
            L_date=(df[df['low']==L_min])['date'].to_list()
            if H_date>L_date:
                price={}
                price['Ticker']=i
                price['L_buy_price']=L_min
                price['H_buy_price']=L_min+(L_min*0.01)
                price['H_sell_price']=H_max
                price['L_sell_price']=H_max-(H_max*0.01)
                price['Current price']= int(get_live_price(i))
                price['profit% ']=((price['L_sell_price']-price['H_buy_price'])/price['H_buy_price'])*100
                buy.append(price)
            elif H_date<L_date:
                price={}
                price['Ticker']=i
                price['H_sell_price']=H_max
                price['L_sell_price']=H_max-(H_max*0.01)
                price['L_buy_price']=L_min
                price['H_buy_price']=L_min+(L_min*0.01)
                price['Current price']= int(get_live_price(i))
                price['profit%']=((price['L_sell_price']-price['H_buy_price'])/price['H_buy_price'])*100
                sell.append(price)
        
        buy_df=pd.DataFrame()
        for i in range (0,len(buy)):
            buy_df=buy_df.append([buy[i]],ignore_index=True)
        buy_df = buy_df[buy_df['profit% '] > 3]
        sell_df=pd.DataFrame()
        for j in range (0,len(sell)):
            sell_df=sell_df.append([sell[j]],ignore_index=True)
        sell_df = sell_df[sell_df['profit%'] > 3]

        return buy_df,sell_df
        

# Portfolio
class Portfolio():
    def __init__(self):
        self.user_name = self.get_user_name()
        self.deta = Deta('d0p5if1f_GSnmoPk32YPhwKaJzN6sq7hM2DN4XPks')
        self.dbp = self.deta.Base('StockyAI_portfolio')
        self.db_tran = self.deta.Base('transactions')
        self.p_data = self.dbp.get(key=self.user_name)
        self.cash = self.p_data['cash']
        self.stocks = self.p_data['stocks']
        self.N50List=tickers_nifty50()
        self.now = dt.datetime.now()
        
        #return self.p_data['cash']
        #self.S_df = pd.DataFrame(columns=['stock','buy_price','quantity'])
        #self.S_df=self.S_df.append(self.stocks,ignore_index=True)
        #print(self.stocks)
        
    def Buy (self,ticker,quant):
        tik= ticker
        #ticker = yf.Ticker(ticker)
        price = get_live_price(tik)
        quant= quant
        amt = price*quant
        if tik in self.stocks.keys():
            h_quant = self.stocks[tik]['quantity']
            h_amt = h_quant*self.stocks[tik]['buy_price']
            if self.cash >= amt:
                self.cash=self.cash-amt
                S_detail={}
                S_detail['quantity'] = h_quant+quant
                S_detail['buy_price']= (h_amt+amt)/(h_quant+quant)
                self.stocks[tik]=S_detail
                #return self.stocks
                self.dbp.put({'key':self.user_name,'cash':self.cash,'stocks':self.stocks})
                #self.Transactions(self.user_name,ticker,price,quant,'Buy')
                st.success('Stocks Brought')   
                return True   
                    
            else:
                st.warning('INSUFICENT BALANCE')
                return False


        else:
            quant= quant
            amt = price*quant
            if self.cash >= amt:
                self.cash=self.cash-amt
                S_detail={}
                S_detail['quantity'] = quant
                S_detail['buy_price']= price
                self.stocks[tik]=S_detail
                #return self.stocks
                self.dbp.put({'key':self.user_name,'cash':self.cash,'stocks':self.stocks})
                #self.Transactions(self.user_name,tik,price,quant,"Buy")
                st.success('Stocks Brought')
                return True
                
            else:
                st.warning('INSUFICENT BALANCE')
                return False

    def Sell (self,ticker,quant):
        tik=ticker
        price = get_live_price(tik)
        quant= quant
        amt = price*quant
        if self.stocks[tik]['quantity']>= quant :
            self.cash=self.cash+amt
            r_quant = self.stocks[tik]['quantity']-quant
            S_details=(self.stocks[tik])
            S_details['quantity']=r_quant
            self.stocks[tik]=S_details
            #print(self.stocks[tik])
            #return self.stocks
            self.dbp.put({'key':self.user_name,'cash':self.cash,'stocks':self.stocks})
            #self.Transactions(self.user_name,tik,price,quant,"Sell")
            st.success('Stocks Sold')
            return True

        elif tik not in self.stocks.keys():
            st.warning("Short sell is not Allowed...!")
            return False

        else:
            st.warning('INSUFICENT Quantity')
            return False


    def get_holdings(self):
        #print(self.p_data['stocks'])
        hold_df = pd.DataFrame(self.p_data['stocks'])
        hold_df=hold_df.transpose()
        hold_df=hold_df.reset_index()
        hold_df['index']=hold_df['index'].astype('str')
        tiks=hold_df['index'].to_list()
        prices=[]
        
        for i in (tiks):
            pr = get_live_price(i)
            prices.append(pr)
            
        #hold_df['current price']=hold_df['index'].apply(self.get_current_price)
        hold_df['Invested Value']=hold_df['buy_price']*hold_df['quantity']
        #hold_df['Value']=hold_df['Value'].apply(lambda x: round(x,2))
        hold_df['current price']=prices
        hold_df['Current Value']=(hold_df['current price'])*(hold_df['quantity'])
        hold_df['P&L']= (hold_df['current price']-hold_df['buy_price'])*hold_df['quantity']
        hold_df['P&L in %']= (hold_df['P&L']/(hold_df['buy_price']*hold_df['quantity']))*100
        hold_df=hold_df[hold_df['quantity']>0]
        amount_in= hold_df['Invested Value'].sum()
        current_amt = hold_df['Current Value'].sum()
        
        hold_df['quantity']=hold_df['quantity'].astype('int')
        return hold_df, self.cash,amount_in,current_amt

    def get_user_name(self):
        User_N=""
        if st.session_state['authentication_status']:
            User_N = st.session_state['username']
        else:
            User_N='dume'

        return User_N

    def Transactions(self,user,ticker,price,quantity,str):
        date = self.now.strftime("%d-%m-%Y")
        trans=self.db_tran.get(key=user)['transaction']
        trans.append({'Date':date,'Ticker':ticker,'Price':price,'Quantity':quantity,'Action':str})
        self.db_tran.put({'key':user,'transaction':trans})

    def Demo_Trans(self,user):
        self.db_tran.put({'key':user,'transaction':[]})


    def get_transactions(self,user):
        tran=self.db_tran.get(key=user)['transaction']
        T_df = pd.DataFrame(tran)
        T_df=T_df[['Date','Ticker','Price','Quantity','Action']]
        return T_df





    

class Store_price():

    def __init__(self):
        self.deta = Deta('d0p5if1f_GSnmoPk32YPhwKaJzN6sq7hM2DN4XPks')
        self.dbh = self.deta.Base('StockyAI_home')

    def save_perv_price(self):
        N50_list=tickers_nifty50()
        N50_price = {}
        N50_price_live = {}
        for i in (N50_list):
            print(i)
            if i == 'MM.NS':
                N50_price[i]=get_quote_data('M&M.NS')['regularMarketChange']
                N50_price_live[i]= get_quote_data('M&M.NS')['regularMarketPrice']
            else:
                N50_price[i]=get_quote_data(i)['regularMarketChange']
                N50_price_live[i]= get_quote_data(i)['regularMarketPrice']
        self.dbh.put({'key':'change','price': N50_price})
        self.dbh.put({'key':'Live','price': N50_price_live})
        return N50_list

    def live_prices(self):
        live =self.dbh.get(key='Live')
        change = self.dbh.get(key='change')
        live = live['price']
        change = change['price']
        return live,change


    def N50_change(self):
        N50List = tickers_nifty50()
        Live_prices=self.dbh.get(key='Live prices')
        Live_pri=Live_prices['price']
        change_price={}
        for i in (N50List):
            change_price[i]=Live_pri[i]-closing_price[i]

        return change_price,N50List,Live_pri

    def stock1Mp(self,ticker):

        tick =yf.Ticker(ticker)
        his = tick.history(period='1mo')
        his=his.reset_index()
        his.drop((['Dividends','Stock Splits']),axis=1,inplace=True)
        his['Date']=pd.to_datetime(his['Date'])
        return his

    def trained_tickers(self,ticker):
        T_list=[]
        T_T=self.dbh.get(key='trained_T')
        T_list = T_T['price']
        T_list.append(ticker)
        T_list=set(T_list)
        T_list = list(T_list)
        self.dbh.put({'key':'trained_T','price':T_list})

    def get_T_tickers(self):
        T_T=self.dbh.get(key='trained_T')
        T_T = T_T['price']
        #T_T = set(T_T)
        return T_T

    def put_tele_user(self,T_user,S_user):
        # T_user telegram user id and S_user is Stocky AI user id
        user_d = self.dbh.get(key='telegram_users')['data']
        user_d[T_user]=S_user
        self.dbh.put({'key':'telegram_users','data':user_d})
        

    def get_tele_user(self):
        data=self.dbh.get(key='telegram_users')['data']
        return data




class Ticker_UI():
    def __init__(self):
        pass

    def Plot(self,ticker):
        today=dt.datetime.now().strftime('%Y-%m-%d')
        u1,u2,u3=st.columns(3)
        u1.header(ticker)
        U_sele=u3.selectbox('Select period',options=('1 month','3 months','6 months','1 year','5 years'))
        E_date=""
        if U_sele == "1 month":
            E_date=(dt.datetime.today()-dt.timedelta(30)).strftime('%Y-%m-%d')
        elif U_sele == '3 months':
            E_date=(dt.datetime.today()-dt.timedelta(91)).strftime('%Y-%m-%d')
        elif U_sele == '6 months':
            E_date=(dt.datetime.today()-dt.timedelta(183)).strftime('%Y-%m-%d')
        elif U_sele == '1 year':
            E_date=(dt.datetime.today()-dt.timedelta(365)).strftime('%Y-%m-%d')
        elif U_sele == '5 years':
            E_date=(dt.datetime.today()-dt.timedelta(1825)).strftime('%Y-%m-%d')

        df=get_data(ticker,start_date=E_date,end_date=today)['close']
        st.line_chart(data=df)

    def Stock_details(self,ticker):
        details = get_quote_data(ticker)
        L_ofItems=['longName','regularMarketChangePercent','regularMarketPrice','fiftyTwoWeekLow','fiftyTwoWeekHigh','fiftyDayAverage','twoHundredDayAverage','regularMarketChange','regularMarketDayHigh','regularMarketDayLow','regularMarketPreviousClose']
        laa = []
        for i in (L_ofItems):
            laa.append(details[i])
        df = pd.DataFrame(laa,index=L_ofItems)
        return df

    def live_stock(self,ticker):
        details=get_quote_data(ticker)
        name = details['longName']
        C_price = round(details['regularMarketPrice'],2)
        C_change = round(details['regularMarketChange'],2)
        return name,C_price,C_change

    def load_lottiurl(self,url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        
        return r.json()



class credintials():
    def __init__(self):
        self.deta = Deta('d0p5if1f_GSnmoPk32YPhwKaJzN6sq7hM2DN4XPks')
        self.dbc = self.deta.Base('credintials')
        self.dbp = self.deta.Base('StockyAI_portfolio')
        self.dbf = self.deta.Base('feedback')
        self.now = dt.datetime.now()

    def credintials_update(self,dictnory):
        self.dbc.put({"key":"credintials",'user':dictnory})
        #self.dbc.put({'key':'credintials','users':{"praveen":{'name':'Praveen Kumar','password':'$2b$12$f3FHtJKI64LUWzhPRiEvU.VOQfwzwfy0mVD.JJU6fkYzTbz5AptKu','email':'praveen9090002135@gmail.com'}}})
        

    def credintials_get(self):
        keys=self.dbc.get(key='credintials')
        credintials=keys['user']
        return credintials

    def creat_portfolio(self,user_name):

        self.dbp.put({'key':user_name,'cash':100000,'stocks':{"demo": {"buy_price": 0,"quantity": 0}}})
                

    def get_feedback(self,name,feedback):
        date = self.now.strftime("%d-%m-%Y")
        self.dbf.put({'key':name,'Date':date,'Feedback':feedback})

    def get_feedback_data(self):
        data=self.dbf.fetch().items
        df = pd.DataFrame(data)
        df=df[['Date','key','Feedback']]
        return df

    def get_users_data(self):
        data=self.dbc.get(key='credintials')
        data=data['user']['usernames']
        df = pd.DataFrame(data)
        df=df.transpose()
        return df


        

