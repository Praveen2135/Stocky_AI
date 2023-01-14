import yfinance as yf
import seaborn as sns
from keras.models import Sequential
from sklearn.preprocessing import StandardScaler
from keras.layers import LSTM
from keras.layers import Dense ,Dropout
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score,mean_absolute_error,accuracy_score, mean_squared_error
from pandas.tseries.offsets import CustomBusinessDay
import matplotlib.pyplot as plt
import datetime as dt
import tensorflow as tf
import Stocky_DB_2
import streamlit as st
from streamlit_lottie import st_lottie

SPP = Stocky_DB_2.Store_price()
SUI = Stocky_DB_2.Ticker_UI()
loader=SUI.load_lottiurl('https://assets7.lottiefiles.com/packages/lf20_gbfwtkzw.json')

class StockyAiTrain:
    
    def __init__(self,ticker):
        self.ticker=ticker
        self.Train_data=""
        self.today=dt.date.today()
        self.T_DF=''
        self.Train_data_scaled=""
        self.trainY_open=''
        self.trainY_high=''
        self.trainY_low=''
        self.trainY_close=''
        self.scaler = StandardScaler()
        self.final_df= pd.DataFrame()
        self.pre_pro_data()
        SPP.trained_tickers(self.ticker)
        self.holidays = ['2023-01-26','2023-03-07','2023-03-30','2023-04-04','2023-04-07','2023-04-14','2023-05-01','2023-06-28','2023-08-15','2023-09-19','2023-10-02','2023-10-24','2023-11-14','2023-11-27','2023-12-25']
        self.Training()
        
    def pre_pro_data(self):
        ticker_obj = yf.Ticker(self.ticker)
        T_DF=ticker_obj.history(period='1y')
        T_DF.drop(['Dividends','Stock Splits','Volume'],axis=1,inplace=True)
        T_DF=T_DF.reset_index()
        T_DF=T_DF[T_DF['Date']>'2000-01-01']
        T_dates = T_DF['Date']
        Train_data=T_DF.drop('Date',axis=1)
        self.T_DF=T_DF
        self.scaler = self.scaler.fit(Train_data)
        Train_data_scaled = self.scaler.transform(Train_data)
        self.Train_data=Train_data
        trainX=[]
        trainY_open=[]
        trainY_high=[]
        trainY_low=[]
        trainY_close=[]
        n_future=1
        n_past=14
        for i in range(n_past, len(Train_data_scaled) - n_future +1):
            trainX.append(Train_data_scaled[i - n_past:i, 0:Train_data.shape[1]])
            trainY_open.append(Train_data_scaled[i + n_future - 1:i + n_future, 0])
            trainY_high.append(Train_data_scaled[i + n_future - 1:i + n_future, 1])
            trainY_low.append(Train_data_scaled[i + n_future - 1:i + n_future, 2])
            trainY_close.append(Train_data_scaled[i + n_future - 1:i + n_future, 3])
        trainX,trainY_open,trainY_high,trainY_low,trainY_close= np.array(trainX),np.array(trainY_open),np.array(trainY_high),np.array(trainY_low),np.array(trainY_close)
        self.trainX=trainX
        self.trainY_open=trainY_open
        self.trainY_high=trainY_high
        self.trainY_low=trainY_low
        self.trainY_close=trainY_close
        
    def Training(self):
        #Sequential for Opening
        model_open = Sequential()
        model_open.add(LSTM(64, activation='relu', input_shape=(self.trainX.shape[1],self.trainX.shape[2]) ,return_sequences=True))
        model_open.add(LSTM(32, activation= 'relu', return_sequences= False))
        model_open.add(Dropout(0.2))
        model_open.add(Dense(self.trainY_open.shape[1]))
        model_open.compile(loss='mse',optimizer='adam')

        #Sequential for High
        model_high = Sequential()
        model_high.add(LSTM(64, activation='relu', input_shape=(self.trainX.shape[1],self.trainX.shape[2]) ,return_sequences=True))
        model_high.add(LSTM(32, activation= 'relu', return_sequences= False))
        model_high.add(Dropout(0.2))
        model_high.add(Dense(self.trainY_high.shape[1]))
        model_high.compile(optimizer='adam', loss='mse')
        
        #Sequential for Low
        model_low = Sequential()
        model_low.add(LSTM(64, activation='relu', input_shape=(self.trainX.shape[1],self.trainX.shape[2]) ,return_sequences=True))
        model_low.add(LSTM(32, activation= 'relu', return_sequences= False))
        model_low.add(Dropout(0.2))
        model_low.add(Dense(self.trainY_low.shape[1]))
        model_low.compile(optimizer='adam', loss='mse')
        
        #Sequential for Close
        model_close = Sequential()
        model_close.add(LSTM(64, activation='relu', input_shape=(self.trainX.shape[1],self.trainX.shape[2]) ,return_sequences=True))
        model_close.add(LSTM(32, activation= 'relu', return_sequences= False))
        model_close.add(Dropout(0.2))
        model_close.add(Dense(self.trainY_close.shape[1]))
        model_close.compile(optimizer='adam', loss='mse')
        
        
        
        # Model Trainging
        c1,c2 = st.columns(2)
        tf.config.run_functions_eagerly(True)
        c1.write('''Opening sctock price training Started....''')
        st_lottie(loader,height=100,width=100, key='loader')
        history_open = model_open.fit(self.trainX, self.trainY_open, epochs=24, batch_size= 12, validation_split= 0.1, verbose =1 )
        c1.write('''Opening sctock price training Ended....''')
        c1.write('''High sctock price training Started....''')
        history_high = model_high.fit(self.trainX, self.trainY_high, epochs=24, batch_size= 12, validation_split= 0.1, verbose =1 )
        c1.write('''High sctock price training Ended....''')
        c1.write('''Low sctock price training Started....''')
        history_low = model_low.fit(self.trainX, self.trainY_low, epochs=24, batch_size= 12, validation_split= 0.1, verbose =1 )
        c1.write('Low sctock price training Ended....')
        c1.write('Closeing sctock price training Started....')
        history_close = model_close.fit(self.trainX, self.trainY_close, epochs=24, batch_size= 12, validation_split= 0.1, verbose =1 )
        c1.write('''Closeing sctock price training Ended....''')
        st.subheader('Training Completed...')
        comp=SUI.load_lottiurl('https://assets5.lottiefiles.com/packages/lf20_uk52xbuq.json')
        st_lottie(comp,height=100,width=100, key='comp')
        SPP.trained_tickers(self.ticker)


        
        #Exporting PKL
        model_open.save('Models/{}_open.h5'.format(self.ticker))
        model_high.save('Models/{}_high.h5'.format(self.ticker))
        model_low.save('Models/{}_low.h5'.format(self.ticker))
        model_close.save('Models/{}_close.h5'.format(self.ticker))

class StockyAIForcast:
    
    def __init__(self,ticker):
        self.ticker = ticker
        self.prediction()
    
    def prediction(self):
        #df_forcast=pd.DataFrame()
        now=dt.datetime.now()
        ticker = self.ticker
        ticker_obj = yf.Ticker(ticker)
        T_DF=ticker_obj.history(period='90d')
        T_DF=T_DF.reset_index()
        T_DF.drop(['Date','Volume','Dividends','Stock Splits'], axis=1,inplace=True)
        scaler = StandardScaler()
        scaled_data=scaler.fit_transform(T_DF)
        scaled_data = np.array(scaled_data)
        trainX=[]
        n_future=1
        n_past=14
        for i in range(n_past, len(scaled_data) - n_future +1):
            trainX.append(scaled_data[i - n_past:i, 0:scaled_data.shape[1]])

        trainX = np.array(trainX)
        holidays = ['2022-01-26','2022-03-01','2022-03-18','2022-04-14','2022-04-15','2022-05-03','2022-08-09','2022-08-15','2022-08-31','2022-10-05','2022-10-26','2022-11-08']
        buz_day=CustomBusinessDay(holidays=holidays)
        n_feature = 30
        forcast_dates = pd.date_range(now.strftime("%Y-%m-%d"), periods= n_feature, freq=buz_day).tolist()
        n_days_for_prediction=n_feature

        model_open = tf.keras.models.load_model('Models/{}_open.h5'.format(ticker))
        model_high = tf.keras.models.load_model('Models/{}_high.h5'.format(ticker))
        model_low = tf.keras.models.load_model('Models/{}_low.h5'.format(ticker))
        model_close = tf.keras.models.load_model('Models/{}_close.h5'.format(ticker))

        prediction_open = model_open.predict(trainX[-n_days_for_prediction:])
        prediction_high = model_high.predict(trainX[-n_days_for_prediction:])
        prediction_low = model_low.predict(trainX[-n_days_for_prediction:])
        prediction_close = model_close.predict(trainX[-n_days_for_prediction:])

        prediction_copies_open = np.repeat(prediction_open, T_DF.shape[1], axis=-1)
        y_pred_future_open = scaler.inverse_transform(prediction_copies_open)[:,0]
        prediction_copies_high = np.repeat(prediction_high, T_DF.shape[1], axis=-1)
        y_pred_future_high = scaler.inverse_transform(prediction_copies_high)[:,0]
        prediction_copies_low = np.repeat(prediction_low, T_DF.shape[1], axis=-1)
        y_pred_future_low = scaler.inverse_transform(prediction_copies_low)[:,0]
        prediction_copies_close = np.repeat(prediction_close, T_DF.shape[1], axis=-1)
        y_pred_future_close = scaler.inverse_transform(prediction_copies_close)[:,0]

        df_forcast = pd.DataFrame({'Date':np.array(forcast_dates),'Open':(y_pred_future_open),'High':(y_pred_future_high),'Low':(y_pred_future_low),'Close':(y_pred_future_close)})
        df_forcast['Date']=pd.to_datetime(df_forcast['Date'])
        print("dONE")
        df_forcast['Date'] = df_forcast['Date'].astype('str')
        SD = Stocky_DB_2.StockyDb()
        SD.save_to_DB(ticker,df_forcast)
      

