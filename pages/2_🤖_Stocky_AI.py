import Stocky_AI
import Stocky_DB_2
import pandas as pd
import plotly.graph_objects as go
import mplfinance as mpf
from yahoo_fin.stock_info import *
import datetime as dt
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_lottie as st_l

SD = Stocky_DB_2.StockyDb()
SP = Stocky_DB_2.Portfolio()
SPP = Stocky_DB_2.Store_price()
SUI = Stocky_DB_2.Ticker_UI()

c1,c2 = st.columns(2)

selected = option_menu(
    menu_title=None,
    options=['Predictions','Predict','Train'],
    icons=["projector-fill","server","terminal"],
    orientation='horizontal',
    styles={'nav-link':{'font-size':'15px'}})
   

if selected == "Predict":
    #st.header("WIP")
    c1,c2,c3 = st.columns(3)
    AI=SUI.load_lottiurl('https://assets6.lottiefiles.com/packages/lf20_itilDAyVNt.json')
    T_T=SPP.get_T_tickers()
    ticker = st.selectbox('Select from trained Tickers',options=(T_T))
    predictB = st.button('Predict')
    #st_lottie(robot,height=250,width=250, key='hello')
    if predictB:
        st_l.st_lottie(AI,height=250,width=250, key='AI')
        Stocky_AI.StockyAIForcast(ticker)
        st.success('Ticker Prediction Done...!')
        

elif selected == 'Train':
    coder=SUI.load_lottiurl('https://assets7.lottiefiles.com/packages/lf20_ne6kcqfz.json')
    ticker=st.text_input('Ticker')
    trainB=st.button('Train')
    if trainB:
        st_l(coder,height=250,width=250, key='coder')
        Stocky_AI.StockyAiTrain(ticker)
        st.success('Stocky AI started Learning abount ticker')
        SPP.trained_tickers(ticker)

elif selected == 'Predictions':
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
