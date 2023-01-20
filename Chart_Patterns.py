# importing all requied modules
import pandas as pd
import numpy as np

# Creating a class which will have all the function which will find the patterns
class chart_patterns():
    def __init__(self) -> None:
        pass

    def Hammer_pattern(self,dict,list):
        data=dict
        tik=list
        df = pd.DataFrame(columns=['Date','Open','High','Low','Close','Ticker'])
        for i in tik:
            stock_data = data[i]
        # Calculate necessary technical indicators
            stock_data['low'] = stock_data['Low']
            stock_data['high'] = stock_data['High']
            stock_data['close'] = stock_data['Close']
            stock_data['open'] = stock_data['Open']
            stock_data['candle_body'] = abs(stock_data['Close'] - stock_data['Open'])
            stock_data['upper_shadow'] = stock_data['High'] - stock_data[['Close','Open']].max(axis=1)
            stock_data['lower_shadow'] = stock_data[['Close','Open']].min(axis=1) - stock_data['low']
            stock_data['hammer'] = (stock_data['candle_body'] < stock_data['upper_shadow']) & (stock_data['lower_shadow'] > (3 * stock_data['candle_body']))

            # Print the rows where hammer is True
            stock_data=stock_data[stock_data['hammer'] == True]
            stock_data=stock_data.reset_index()
            stock_data=stock_data[['Date','Open','High','Low','Close']]
            stock_data['Date']=pd.to_datetime(stock_data['Date'])
            stock_data['Date']=stock_data['Date'].dt.strftime('%m-%d-%Y')
            stock_data['Ticker']=i
            if len(stock_data) >0:
                print(i)
                df=df.append(stock_data,ignore_index=True)
                print('___________________________________________________________')
        return df

    def bullish_engulfing(df):
        stock_data=df
        # Calculate necessary technical indicators
        stock_data["previous_close"] = stock_data["Close"].shift(1)
        stock_data["previous_open"] = stock_data["Open"].shift(1)

        # Bullish Engulfing condition
        stock_data["bullish_engulfing"] = ((stock_data["Open"] < stock_data["previous_open"]) & (stock_data["Close"] > stock_data["previous_close"]))

        # Print the rows where bullish engulfing is True
        stock_data=stock_data[stock_data["bullish_engulfing"] == True]
        return stock_data