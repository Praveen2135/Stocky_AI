# importing all require modules
import yfinance as yf
import pandas as pd
import streamlit as st
import Chart_Patterns

CP = Chart_Patterns.chart_patterns()

#list of tickers for whitch parterns will found
multi_tic = 'ADANIENT.NS APOLLOHOSP.NS BAJAJ-AUTO.NS BAJAJFINSV.NS BAJFINANCE.NS BHARTIARTL.NS BRITANNIA.NS CIPLA.NS COALINDIA.NS HDFCLIFE.NS HEROMOTOCO.NS HINDALCO.NS ICICIBANK.NS INDUSINDBK.NS ITC.NS KOTAKBANK.NS LT.NS MARUTI.NS NESTLEIND.NS NTPC.NS ONGC.NS RELIANCE.NS TATACONSUM.NS TATASTEEL.NS TCS.NS TECHM.NS TITAN.NS ULTRACEMCO.NS WIPRO.NS'

# Creating object for all tickers in the list
N50_obj = yf.Tickers(multi_tic)
# getting the tickers name from created object
tik=N50_obj.tickers.keys()

#Empty DIC for storying all tickers data 
data={}
#for loop for getting all tickers 7days data 
for i in tik:
  i_tic=i
  i_tic = i_tic.split(".")[0]
  print(i_tic)
  #print(i)
  i_tic=N50_obj.tickers[i]
  df=i_tic.history(period='7d')
  data['{}'.format(i)]=df


st.subheader('Selected Patter search for last 7days in Nifty50 Stocks')
select = st.selectbox('Chart Patterns',options=['Hammer pattern','Bullish Engulfing','Bearish Engulfing','Shooting Star','Bullish Harami','Bearish Harami'])

if select == 'Hammer pattern':
  df=CP.Hammer_pattern(data,tik)

elif select == 'Bullish Engulfing':
  df=CP.bullish_engulfing(data,tik)

elif select == 'Bearish Engulfing':
  df=CP.bearish_engulfing(data,tik)

elif select == 'Shooting Star':
  df = CP.Shooting_star(data,tik)

elif select == 'Bullish Harami':
  df= CP.Bullish_Harami(data,tik)

elif select == 'Bearish Harami':
  df= CP.Bearish_Harami(data,tik)

st.table(df)
