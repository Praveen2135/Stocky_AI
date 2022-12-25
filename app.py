import streamlit as st
import Stocky_AI
import Stocky_DB_2
import pandas as pd
import plotly.graph_objects as go
import mplfinance as mpf
from yahoo_fin.stock_info import *
import datetime as dt
#from tensorflow.keras.utils import HDF5Matrix


SD = Stocky_DB_2.StockyDb()
SP = Stocky_DB_2.Portfolio()
SPP = Stocky_DB_2.Store_price()

now=dt.datetime.now()
while now.strftime("%H:%M") == '22:00' :
    SPP.save_perv_price()
    break

# UI 
# TRain and Predict Choies
main_choies = st.radio("CHOISE ONE",options=('Home',"Predict","Train","Predictions",'Recomendation','Portfolio'))

if main_choies == "Predict":
    st.header("WIP")
    ticker=st.text_input('Ticker')
    predictB = st.button('Predict')
    if predictB:
        Stocky_AI.StockyAIForcast(ticker)
        st.success("Pridiction done for ticker")
        
elif main_choies == 'Home':
    c1,c2,c3,c4,c5 = st.columns(5)
    #c1.metric(label=N50_list[0],value=N50_price[N50_list[0]])
    #c2.metric(label=N50_list[1],value=N50_price[N50_list[1]])
    #c3.metric(label=N50_list[2],value=N50_price[N50_list[2]])
    #c4.metric(label=N50_list[3],value=N50_price[N50_list[3]])
    #c5.metric(label=N50_list[4],value=N50_price[N50_list[4]])

    #style_metric_cards(border_left_color='#1E1E1E')

elif main_choies == 'Train':
    ticker=st.text_input('Ticker')
    trainB=st.button('Train')
    if trainB:
        Stocky_AI.StockyAiTrain(ticker)
        st.success('Stocky AI started Learning abount ticker')
    #st.success('Stocky AI Learned abount the ticker, now you can go to pridct')

elif main_choies == 'Predictions':
    tick_list = SD.get_all_ticker()
    T_selected = st.selectbox("Tickers",options=tick_list)
    showB=st.button("Show")
    if showB:
        T_df= pd.DataFrame(SD.ticker_df(T_selected))
        T_df = T_df[['date','open','high','low','close']]
        st.header(T_selected)
        #st.table(T_df)
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=T_df['date'],open=T_df['open'],high=T_df['high'],low=T_df['low'],close=T_df['close']))
        st.plotly_chart(fig)

elif main_choies == 'Recomendation':
    buy_df,sell_df=SD.Recomodation()
    st.header('For Buy')
    st.table(buy_df)
    st.header('For Sell')
    st.table(sell_df)

elif main_choies == 'Portfolio':
    holdings, cash=SP.get_holdings()
    st.header('Praveen')
    st.subheader('Availabel cash ')
    st.subheader(cash)
    st.table(holdings)
    BorS=st.selectbox('Buy or Sell Action',options=['','Buy','Sell'])
    if BorS == 'Buy':
        ticker=st.text_input('Ticker')
        quant=st.number_input('Quantity',min_value=1,step=1)
        S_but=st.button('Proced')
        if S_but :
            SP.Buy(ticker,quant)

    elif BorS == 'Sell':
        ticker=st.text_input('Ticker')
        quant=st.number_input('Quantity',min_value=1,step=1)
        S_but=st.button('Proced')
        if S_but :
            SP.Sell(ticker,quant)
            

