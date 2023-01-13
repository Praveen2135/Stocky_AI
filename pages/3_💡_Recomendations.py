import streamlit as st
import Stocky_DB_2

SD = Stocky_DB_2.StockyDb()

if st.session_state['authentication_status']:

    buy_df,sell_df=SD.Recomodation()
    st.header('For Buy')
    st.table(buy_df)
    st.header('For Sell')
    st.table(sell_df)

else:
    st.warning('Please login')