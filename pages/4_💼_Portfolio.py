import Stocky_DB_2
import pandas as pd
import plotly.graph_objects as go
import mplfinance as mpf
from yahoo_fin.stock_info import *
import datetime as dt
import streamlit as st

if st.session_state == {}:
    st.session_state['authentication_status'] = ""
    
SP = Stocky_DB_2.Portfolio()
SUI = Stocky_DB_2.Ticker_UI()


if st.session_state['authentication_status']:
    holdings, cash=SP.get_holdings()
    st.header(st.session_state['name'])
    user=st.session_state['username']
    st.subheader('Availabel cash ')
    st.subheader(int(cash))
    st.table(holdings)
    p1,p2,p3 = st.columns(3)
    p4,p5,p6 = st.columns(3)
    BorS=p1.selectbox('Buy or Sell Action',options=['','Buy','Sell'])
    T_button=p4.button('Transactions')
    if T_button:
        T_df=SP.get_transactions(user)
        st.table(T_df)
        
    if BorS == 'Buy':
        B_ticker=p2.text_input('Ticker')
        if B_ticker == "":
            st.warning('Please Enter Ticker and Press Enter')
            #st.metric(label=ticker,value= get_live_price(ticker))
        else:
            name,C_price,C_change=SUI.live_stock(B_ticker)
            st.metric(label=name,value=C_price,delta=C_change)
            quant=p3.number_input('Quantity',min_value=1,step=1)
            S_but=st.button('Proced')
            if S_but :
                SP.Buy(B_ticker,quant)
                SP.Transactions(user,B_ticker,C_price,quant,'Buy')
                st.experimental_rerun()
                

    elif BorS == 'Sell':
        S_ticker=p2.text_input('Ticker')
        if S_ticker == "":
            st.warning('Please Enter Ticker and Press Enter')
            #st.metric(label=ticker,value= get_live_price(ticker))
        else:
            name,C_price,C_change=SUI.live_stock(S_ticker)
            st.metric(label=name,value=C_price,delta=C_change)
            quant=p3.number_input('Quantity',min_value=1,step=1)
            S_but=st.button('Proced')
            if S_but :
                SP.Sell(S_ticker,quant)
                SP.Transactions(user,S_ticker,C_price,quant,'Sell')
                st.experimental_rerun()

else:
    st.warning('Please login')
    
    