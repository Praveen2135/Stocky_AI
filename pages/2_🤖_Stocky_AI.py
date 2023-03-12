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
import sqlite3

#Starting SQLite
conn = sqlite3.connect("data.db")

if st.session_state == {}:
    st.session_state['authentication_status'] = ""

# To show name on side bar
if st.session_state['authentication_status']:
    st.sidebar.header(st.session_state['name'])

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
    prd_all = st.button('Pridect ALL')
    st.write("Note:- If Ticker is not availabile in Drop-down, Please Go-to Train and Train the Stocky AI.")
    #st_lottie(robot,height=250,width=250, key='hello')
    if predictB:
        st_l.st_lottie(AI,height=250,width=250, key='AI')
        try:
            Stocky_AI.StockyAIForcast(ticker)
            st.success('Ticker Prediction Done...!')
        except:
            st.warning(f"The ticker {ticker} Was not available, So please train it.")

    if prd_all:
        st_l.st_lottie(AI,height=250,width=250, key='AI')
        for i in T_T:
            print(i,'WIP')
            try:
                Stocky_AI.StockyAIForcast(i)
            except:
                st.warning(f"The ticker {i} Was not available, So please train it.")
            print(i,'Done')
        buy_df,sell_df=SD.Recomodation()
        buy_df.to_csv("buy_df.csv")
        sell_df.to_csv("sell_df.csv")

        st.success('Ticker Prediction Done...!')
        

elif selected == 'Train':
    coder=SUI.load_lottiurl('https://assets7.lottiefiles.com/packages/lf20_ne6kcqfz.json')
    ticker=st.text_input('Ticker')
    trainB=st.button('Train')
    train_all=st.button('Train All Trained Tickers')
    #st.write('''Note:- Please enter the Ticker as per Yahoo Finance and click on Train,
                        #If you want you can Quit it can train it self.
                        #You will get your ticker in Pridect Drop-down if its Trained''')
                        
    st.write('''Note:- Please enter the Ticker as per Yahoo Finance and click on Train''')

    if trainB:
        SPP.trained_tickers(ticker)
        st_l.st_lottie(coder,height=250,width=250, key='coder')
        try:
            Stocky_AI.StockyAiTrain(ticker)
            st.success('Stocky AI started Learning abount ticker')
        except:
            st.warning("Somthing went wrong, Please  reach out Admin")

    if train_all:
        T_T=SPP.get_T_tickers()
        st_l.st_lottie(coder,height=250,width=250, key='coder')
        for i in T_T:
            try:
                Stocky_AI.StockyAiTrain(i)
                SPP.trained_tickers(i)
                st.success('Stocky AI started Learning abount ticker')
            except:
                st.warning("Somthing went wrong, Please  reach out Admin")

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
    st.write("Note:- Here all predtcted Stock Prices are available.")
    st.write("If you want to pridect the price from today, Please go-to Pridict")
    st.write("If you want to Train Stocky AI on any new stock Go-to Train")