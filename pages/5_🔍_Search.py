import streamlit as st
import Stocky_DB_2


SUI = Stocky_DB_2.Ticker_UI()

ticker=st.sidebar.text_input("Search Ticker")

if ticker == "":
    st.warning('Please enter Ticker')

else:
    SUI.Plot(ticker)
    df = SUI.Stock_details(ticker)
    st.table(df)