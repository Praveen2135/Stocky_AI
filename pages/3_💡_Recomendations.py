import streamlit as st
import Stocky_DB_2
import sqlite3
import pandas as pd
from yahoo_fin.stock_info import *

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

if st.session_state == {}:
    st.session_state['authentication_status'] = ""

# To show name on side bar
if st.session_state['authentication_status']:
    st.sidebar.header(st.session_state['name'])
    
SD = Stocky_DB_2.StockyDb()

if st.session_state['authentication_status']:

    buy_df=pd.read_csv("buy_df.csv")
    sell_df=pd.read_csv("sell_df.csv")
    
    buy_df['Current price'] = buy_df['Ticker'].apply(lambda x : get_live_price(x))
    sell_df['Current price'] = sell_df['Ticker'].apply(lambda x : get_live_price(x))

    buy_df['profit%']=((buy_df['L_sell_price']-buy_df['H_buy_price'])/buy_df['H_buy_price'])*100
    sell_df['profit%']=((sell_df['L_sell_price']-sell_df['H_buy_price'])/sell_df['H_buy_price'])*100
    
    buy_df= (buy_df[buy_df['L_buy_price'] < buy_df['Current price']])
    sell_df= (sell_df[sell_df['L_sell_price'] < sell_df['Current price']])

    buy_df= buy_df[buy_df['profit%']>= 4]
    sell_df= sell_df[sell_df['profit%']>= 4]

    buy_df = buy_df.drop(columns='Unnamed: 0',axis=1)
    sell_df = sell_df.drop(columns='Unnamed: 0',axis=1)

    st.header('For Buy')
    st.table(buy_df)
    st.header('For Sell')
    st.table(sell_df)

else:
    st.warning('Please login')