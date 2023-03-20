import streamlit as st
import Stocky_DB_2
from yahoo_fin.stock_info import *
from streamlit_option_menu import option_menu


SUI = Stocky_DB_2.Ticker_UI()

ticker=st.sidebar.text_input("Search Ticker")


try:
    if ticker == "":
        st.warning('Please enter Ticker')

    else:
        SUI.Plot(ticker)
        selected = option_menu(
        menu_title=None,
        options=['Valuation','Prices'],
        orientation='horizontal',
        styles={'nav-link':{'font-size':'15px'}})

        if selected == 'Valuation':
            valu_df=get_stats_valuation(ticker)
            st.table(valu_df)

        elif selected == 'Prices':
            df = SUI.Stock_details(ticker)
            st.table(df)

except:
    st.warning("Please provide right ticker and as per Yahoo Finance")