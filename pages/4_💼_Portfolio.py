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
    holdings, cash,amount_in,current_amt=SP.get_holdings()
    st.header(st.session_state['name'])
    user=st.session_state['username']
    st.subheader('Availabel cash ')
    st.subheader(int(cash))
    t1,t2,t3,t4 = st.columns(4)
    v1,v2,v3,v4 = st.columns(4)
    net_PL =current_amt-amount_in
    t1.subheader('Invested')
    t2.subheader('Current Value')
    t3.subheader('Net P&L')
    t4.subheader('Net P&L %')
    v1.subheader(int(amount_in))
    v2.subheader(int(current_amt))
    v3.subheader(int(net_PL))
    v4.subheader(round(net_PL/amount_in,2))
    holdings = holdings.drop(['Invested Value','Current Value'],axis=1)
    st.table(holdings)
    p4,p5,p6 = st.columns(3)
    T_button=p4.button('Transactions')
    p1,p2,p3 = st.columns(3)
    
    BorS=p1.selectbox('Buy or Sell Action',options=['','Buy','Sell'])
    
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
                action=SP.Buy(B_ticker,quant)
                if action:
                    SP.Transactions(user,B_ticker,C_price,quant,"Buy")
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
                action=SP.Sell(S_ticker,quant)
                if action:
                    SP.Transactions(user,S_ticker,C_price,quant,"Sell")
                st.experimental_rerun()

else:
    st.warning('Please login')
    
    