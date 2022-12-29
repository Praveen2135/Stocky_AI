import Stocky_AI
import Stocky_DB_2
import pandas as pd
import plotly.graph_objects as go
import mplfinance as mpf
from yahoo_fin.stock_info import *
import datetime as dt
import streamlit as st
#from tensorflow.keras.utils import HDF5Matrix


SD = Stocky_DB_2.StockyDb()
SP = Stocky_DB_2.Portfolio()
SPP = Stocky_DB_2.Store_price()
SUI = Stocky_DB_2.Ticker_UI()

# UI 
# TRain and Predict Choies
with st.sidebar:
    st.header('Go-To')
    main_choies = st.radio("",options=('Home',"Predict","Train","Predictions",'Recomendation','Portfolio','Search'))

#main_choies = st.radio("CHOISE ONE",options=('Home',"Predict","Train","Predictions",'Recomendation','Portfolio'))

if main_choies == "Predict":
    #st.header("WIP")
    ticker=st.text_input('Ticker')
    predictB = st.button('Predict')
    if predictB:
        Stocky_AI.StockyAIForcast(ticker)
        st.success("Pridiction done for ticker")
        
elif main_choies == 'Home':
    c51,c52,c53 = st.columns(3)
    index=(c51.selectbox('Index',options=('^NSEI','^NSEBANK','^BSESN')))
    c52.metric(label='^NSEI',value=int(get_live_price('^NSEI')),delta=get_quote_data('^NSEI')['regularMarketChange'])
    c53.metric(label='^BSESN',value=int(get_live_price('^BSESN')),delta=get_quote_data('^BSESN')['regularMarketChange'])

    
    his=SPP.stock1Mp(index)
    fig1 = go.Figure()
    fig1.add_trace(go.Candlestick(x=his['Date'],open=his['Open'],high=his['High'],low=his['Low'],close=his['Close']))
    st.plotly_chart(fig1)

    #change_price,N50_list,N50Live=SPP.N50_change()
    N50_list = tickers_nifty50()
    N50Live,change_price = SPP.live_prices()
    c0,c1,c2,c3,c4 = st.columns(5)
    c0.metric(label=N50_list[0],value=int(N50Live[N50_list[0]]),delta=int(change_price[N50_list[0]]))
    c1.metric(label=N50_list[1],value=int(N50Live[N50_list[1]]),delta=int(change_price[N50_list[1]]))
    c2.metric(label=N50_list[2],value=int(N50Live[N50_list[2]]),delta=int(change_price[N50_list[2]]))
    c3.metric(label=N50_list[3],value=int(N50Live[N50_list[3]]),delta=int(change_price[N50_list[3]]))
    c4.metric(label=N50_list[4],value=int(N50Live[N50_list[4]]),delta=int(change_price[N50_list[4]]))

    c5,c6,c7,c8,c9 = st.columns(5)
    c5.metric(label=N50_list[5],value=int(N50Live[N50_list[5]]),delta=int(change_price[N50_list[5]]))
    c6.metric(label=N50_list[6],value=int(N50Live[N50_list[6]]),delta=int(change_price[N50_list[6]]))
    c7.metric(label=N50_list[7],value=int(N50Live[N50_list[7]]),delta=int(change_price[N50_list[7]]))
    c8.metric(label=N50_list[8],value=int(N50Live[N50_list[8]]),delta=int(change_price[N50_list[8]]))
    c9.metric(label=N50_list[9],value=int(N50Live[N50_list[9]]),delta=int(change_price[N50_list[9]]))

    c10,c11,c12,c13,c14 = st.columns(5)
    c10.metric(label=N50_list[10],value=int(N50Live[N50_list[10]]),delta=int(change_price[N50_list[10]]))
    c11.metric(label=N50_list[11],value=int(N50Live[N50_list[11]]),delta=int(change_price[N50_list[11]]))
    c12.metric(label=N50_list[12],value=int(N50Live[N50_list[12]]),delta=int(change_price[N50_list[12]]))
    c13.metric(label=N50_list[13],value=int(N50Live[N50_list[12]]),delta=int(change_price[N50_list[13]]))
    c14.metric(label=N50_list[14],value=int(N50Live[N50_list[13]]),delta=int(change_price[N50_list[14]]))

    c15,c16,c17,c18,c19 = st.columns(5)
    c15.metric(label=N50_list[15],value=int(N50Live[N50_list[15]]),delta=int(change_price[N50_list[15]]))
    c16.metric(label=N50_list[16],value=int(N50Live[N50_list[16]]),delta=int(change_price[N50_list[16]]))
    c17.metric(label=N50_list[17],value=int(N50Live[N50_list[17]]),delta=int(change_price[N50_list[17]]))
    c18.metric(label=N50_list[18],value=int(N50Live[N50_list[18]]),delta=int(change_price[N50_list[18]]))
    c19.metric(label=N50_list[19],value=int(N50Live[N50_list[19]]),delta=int(change_price[N50_list[19]]))

    c20,c21,c22,c23,c24 = st.columns(5)
    c20.metric(label=N50_list[20],value=int(N50Live[N50_list[20]]),delta=int(change_price[N50_list[20]]))
    c21.metric(label=N50_list[21],value=int(N50Live[N50_list[21]]),delta=int(change_price[N50_list[21]]))
    c22.metric(label=N50_list[22],value=int(N50Live[N50_list[22]]),delta=int(change_price[N50_list[22]]))
    c23.metric(label=N50_list[23],value=int(N50Live[N50_list[23]]),delta=int(change_price[N50_list[23]]))
    c24.metric(label=N50_list[24],value=int(N50Live[N50_list[24]]),delta=int(change_price[N50_list[24]]))
    
    c25,c26,c27,c28,c29 = st.columns(5)
    c25.metric(label=N50_list[25],value=int(N50Live[N50_list[25]]),delta=int(change_price[N50_list[25]]))
    c26.metric(label=N50_list[26],value=int(N50Live[N50_list[26]]),delta=int(change_price[N50_list[26]]))
    c27.metric(label=N50_list[27],value=int(N50Live[N50_list[27]]),delta=int(change_price[N50_list[27]]))
    c28.metric(label=N50_list[28],value=int(N50Live[N50_list[28]]),delta=int(change_price[N50_list[28]]))
    c29.metric(label=N50_list[29],value=int(N50Live[N50_list[29]]),delta=int(change_price[N50_list[29]]))


    #style_metric_cards(border_left_color='#1E1E1E')
    ref_b=st.button("Refreash Live Prices")
    if ref_b:
        SPP.save_perv_price()
        st.experimental_rerun()

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
    st.subheader(int(cash))
    st.table(holdings)
    p1,p2,p3 = st.columns(3)
    BorS=p1.selectbox('Buy or Sell Action',options=['','Buy','Sell'])
    if BorS == 'Buy':
        B_ticker=p2.text_input('Ticker')
        if B_ticker == "":
            st.warning('Please Enter Ticker and Press Enter')
            #st.metric(label=ticker,value= get_live_price(ticker))
        else:
            st.metric(label=B_ticker,value= int(get_live_price(B_ticker)))
            quant=p3.number_input('Quantity',min_value=1,step=1)
            S_but=st.button('Proced')
            if S_but :
                SP.Buy(B_ticker,quant)
                st.experimental_rerun()

    elif BorS == 'Sell':
        S_ticker=p2.text_input('Ticker')
        if S_ticker == "":
            st.warning('Please Enter Ticker and Press Enter')
            #st.metric(label=ticker,value= get_live_price(ticker))
        else:
            st.metric(label=S_ticker,value= int(get_live_price(S_ticker)))
            quant=p3.number_input('Quantity',min_value=1,step=1)
            S_but=st.button('Proced')
            if S_but :
                SP.Sell(S_ticker,quant)
                st.experimental_rerun()
            

elif main_choies == 'Search':
    ticker=st.sidebar.text_input("Search Ticker")

    if ticker == "":
        st.warning('Please enter Ticker')

    else:
        SUI.Plot(ticker)
        df = SUI.Stock_details(ticker)
        st.table(df)