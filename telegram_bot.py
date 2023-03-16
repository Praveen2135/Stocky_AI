import telegram
from telegram.ext import *
import Stocky_DB_2
from yahoo_fin.stock_info import *
from deta import Deta
import Stocky_AI

# creating obj for portfolio
#SP = Stocky_DB_2.Portfolio()
STU = Stocky_DB_2.Store_price()
STR= Stocky_DB_2.StockyDb()
STF = Stocky_DB_2.credintials()

data = STU.get_tele_user()

#if st.session_state == {}:
    #st.session_state['authentication_status'] = ""

def T_get_holdings(user_name):
    #print(self.p_data['stocks'])
    deta = Deta('d0p5if1f_GSnmoPk32YPhwKaJzN6sq7hM2DN4XPks')
    dbp = deta.Base('StockyAI_portfolio')
    p_data = dbp.get(key=user_name)
    hold_df = pd.DataFrame(p_data['stocks'])
    hold_df=hold_df.transpose()
    hold_df=hold_df.reset_index()
    hold_df['index']=hold_df['index'].astype('str')
    tiks=hold_df['index'].to_list()
    prices=[]
    
    for i in (tiks):
        pr = get_live_price(i)
        prices.append(pr)
        
    #hold_df['current price']=hold_df['index'].apply(self.get_current_price)
    hold_df['Invested Value']=hold_df['buy_price']*hold_df['quantity']
    #hold_df['Value']=hold_df['Value'].apply(lambda x: round(x,2))
    hold_df['current price']=prices
    hold_df['Current Value']=(hold_df['current price'])*(hold_df['quantity'])
    hold_df['P&L']= (hold_df['current price']-hold_df['buy_price'])*hold_df['quantity']
    hold_df['P&L in %']= (hold_df['P&L']/(hold_df['buy_price']*hold_df['quantity']))*100
    hold_df=hold_df[hold_df['quantity']>0]
    amount_in= hold_df['Invested Value'].sum()
    current_amt = hold_df['Current Value'].sum()
    
    hold_df['quantity']=hold_df['quantity'].astype('int')
    return hold_df,amount_in,current_amt

#this function is to get feedback when any one gives feed back
def get_feedback(user_name,feedback):
    bot=telegram.Bot(token='5900892098:AAEHsv03l9Ow7LOc80re1ESq-sMu6VOvCXs')
    chat_id =1015374223
    bot.send_message(chat_id=chat_id,text=(f'User- {user_name},feedback- {feedback}'))



class Telegram_bot():
    def __init__(self):
        self.Token='5900892098:AAEHsv03l9Ow7LOc80re1ESq-sMu6VOvCXs'
        self.bot = telegram.Bot(token=self.Token)
        self.main()
        
    def start(self,update,context):
        user = update.message.from_user
        username = user.username
        update.message.reply_text("""Welcome to StockyAI, an advanced stock analysis tool powered by machine learning. Our platform offers a comprehensive analysis of various stocks and helps you make informed investment decisions.

In addition to our web app, we also have a Telegram bot that can help you stay up-to-date with the latest stock market trends. Our Telegram bot can send you notifications on the latest stock prices, news, and performance updates, directly to your Telegram chat.

With StockyAI's Telegram bot, you can easily access stock information on-the-go, and make informed investment decisions. Some of the functionalities of our Telegram bot include:

    Stock price updates: Get real-time updates on stock prices, directly in your Telegram chat.

    News updates: Stay informed with the latest news and developments related to your stocks, as soon as it becomes available.

    Stock performance analysis: Get a comprehensive analysis of the performance of various stocks and stay ahead of the market trends.

    Customized alerts: Set custom alerts for your stocks and receive notifications when the price reaches a certain level or when important news is released.

Whether you're a seasoned investor or just starting out, StockyAI's Telegram bot is the perfect tool to help you make informed investment decisions and stay ahead of the market trends. Try it out today!


Please click here to explor
/help""")

    def help(self,update,context):
        update.message.reply_text("""
        The following commands are available:
        /start
        /get_holdings
        /Recomndation
        /stock ticker (as per Yfinance)
        /Train ticker (as per Yfinance)
        /Train_All re-train all ticker
        /Pred_all for predict all tickers trained
        /Feedback your feedback""")

    def reco(self,update, context):
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

        for index, row in buy_df.iterrows():
            update.message.reply_text(f"{row}")
        update.message.reply_text('Sell Side')
        for index, row in sell_df.iterrows():
            update.message.reply_text(f"{row}")

    def stock(self,update, context):
        price = get_live_price(context.args[0])
        price= round(price,2)
        update.message.reply_text(f"Stock price: {price}")

    def login(self,update,context):
        update.message.reply_text("Please give user name")
        user=(update.message)
        update.message.reply_text(user)

    def feedback(self,update,context):
        user = update.message.from_user
        username = user.username
        name = data[username]
        feedback =context.args
        feedback = ' '.join(feedback)
        STF.get_feedback(name,feedback)
        get_feedback(name,feedback)
        update.message.reply_text(f"Thanks for the valuable feedback  {name} .")

    def Train(self,update,context):
        ticker=context.args[0]
        update.message.reply_text(f"""Training is started for {ticker}, It will take 3 to 5 min, will update you once its Done! """)
        Stocky_AI.StockyAiTrain(ticker)
        update.message.reply_text(f"Training for {ticker} is completed")
    
    def Pred_all(self,update,context):
        T_T=STU.get_T_tickers()
        update.message.reply_text('Pridictions for all tickers are started...')
        for i in T_T:
            try:
                Stocky_AI.StockyAIForcast(i)
                update.message.reply_text(f'Pridictions for ticker {i} is Done...')
            except:
                update.message.reply_text(f"The ticker {i} Was not available, So please train it.")
        buy_df,sell_df=SD.Recomodation()
        buy_df.to_csv("buy_df.csv")
        sell_df.to_csv("sell_df.csv")
        update.message.reply_text("Pridictions for all tickers are Done...!")

    def Train_All(self,update,context):
        T_T=STU.get_T_tickers()
        for i in T_T:
            try:
                update.message.reply_text(f'Stocky AI started Learning abount ticker - {i}')
                Stocky_AI.StockyAiTrain(i)
                STU.trained_tickers(i)
                update.message.reply_text(f'Training is done for ticker - {i}')
                
            except:
                update.message.reply_text("Somthing went wrong, Please  reach out Admin")

        update.message.reply_text('Stocky AI Learned abount all ticker...!')

    def get_holdings(self,update, context):
        user = update.message.from_user
        username = user.username
        print(username)
        #Get the user data
        if username in data.keys():
            hold_df,amount_in,current_amt = T_get_holdings(data[username])
            hold_df=hold_df[['index','quantity','P&L in %']]
            #update.message.reply_text(f"we got you {data[username]},your holdings :-")
            for index, row in hold_df.iterrows():
                update.message.reply_text(f"{row}")
        else:
            update.message.reply_text("""Currently you dont have accses
            Sign up here :- https://stockyai.streamlit.app/Sign_In 
            If already Signed up please rigester your Telegram Userid with us""")



    def buy_stock():
        pass

    def sell_stock():
        pass

    def main(self):
        updater = telegram.ext.Updater(self.Token,use_context=True)
        disp = updater.dispatcher
        disp.add_handler(telegram.ext.CommandHandler("start",self.start))
        disp.add_handler(telegram.ext.CommandHandler("help",self.help))
        disp.add_handler(telegram.ext.CommandHandler("login",self.login))
        disp.add_handler(telegram.ext.CommandHandler("stock",self.stock))
        disp.add_handler(telegram.ext.CommandHandler("get_holdings",self.get_holdings))
        disp.add_handler(telegram.ext.CommandHandler("Recomndation",self.reco))
        disp.add_handler(telegram.ext.CommandHandler("Feedback",self.feedback))
        disp.add_handler(telegram.ext.CommandHandler("Train",self.Train))
        disp.add_handler(telegram.ext.CommandHandler("Train_ALL",self.Train_All))
        disp.add_handler(telegram.ext.CommandHandler("Predect_All",self.Pred_all))
        updater.start_polling()
        updater.idle()
