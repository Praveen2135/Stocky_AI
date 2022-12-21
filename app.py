import streamlit as st
import Stocky_AI
import Stocky_DB_2
import pandas as pd
#from tensorflow.keras.utils import HDF5Matrix


# UI 
# TRain and Predict Choies
main_choies = st.radio("CHOISE ONE",options=("Predict","Train","Predictions"))

if main_choies == "Predict":
    st.header("WIP")
    ticker=st.text_input('Ticker')
    predictB = st.button('Predict')
    if predictB:
        Stocky_AI.StockyAIForcast(ticker)
        #Stocky_DB_2.StockyDataBase.save_to_DB(ticker,df_forcast)
        


elif main_choies == 'Train':
    ticker=st.text_input('Ticker')
    trainB=st.button('Train')
    if trainB:
        Stocky_AI.StockyAiTrain(ticker)

    print(ticker)

elif main_choies == 'Predictions':
    SD = Stocky_DB_2.StockyDb()
    tick_list = SD.get_all_ticker()
    T_selected = st.selectbox("Tickers",options=tick_list)
    showB=st.button("Show")
    if showB:
        T_df= pd.DataFrame(SD.ticker_df(T_selected))
        T_df = T_df[['date','open','high','low','close']]
        st.header(T_selected)
        st.table(T_df)



