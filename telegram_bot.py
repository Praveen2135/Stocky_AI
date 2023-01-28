import telegram
from telegram.ext import *
import Stocky_DB_2
from yahoo_fin.stock_info import *

# creating obj for portfolio
#SP = Stocky_DB_2.Portfolio()
STU = Stocky_DB_2.Store_price()

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

class Telegram_bot():
    def __init__(self):
        self.Token='5900892098:AAEHsv03l9Ow7LOc80re1ESq-sMu6VOvCXs'
        self.main()
        

    def start(self,update,context):
        update.message.reply_text("hello praveen")

    def help(self,update,context):
        update.message.reply_text("""
        The following commands are available:
        /start
        /get_holdings
        /stock ticker
        /login""")

    def stock(self,update, context):
        price = get_live_price(context.args[0])
        price= round(price,2)
        update.message.reply_text(f"Stock price: {price}")

    def login(self,update,context):
        update.message.reply_text("Please give user name")
        user=(update.message)
        update.message.reply_text(user)

    def get_holdings(self,update, context):
        user = update.message.from_user
        username = user.username
        print(username)
        #Get the user data
        if username in data.keys():
            hold_df,amount_in,current_amt = T_get_holdings(data[username])
            hold_df=hold_df[['index','quantity','P&L in %']]
            S_DF = hold_df.to_string
            update.message.reply_text(f"we got you {data[username]},your holdings {S_DF} ")
        else:
            update.message.reply_text("Currently you dont have accses")

        

    def main(self):
        updater = telegram.ext.Updater(self.Token,use_context=True)
        disp = updater.dispatcher
        disp.add_handler(telegram.ext.CommandHandler("start",self.start))
        disp.add_handler(telegram.ext.CommandHandler("help",self.help))
        disp.add_handler(telegram.ext.CommandHandler("login",self.login))
        disp.add_handler(telegram.ext.CommandHandler("stock",self.stock))
        disp.add_handler(telegram.ext.CommandHandler("get_holdings",self.get_holdings))
        updater.start_polling()
        updater.idle()