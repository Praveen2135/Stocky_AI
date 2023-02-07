import telegram
from telegram.ext import *
import Stocky_DB_2
from yahoo_fin.stock_info import *
from deta import Deta

# creating obj for portfolio
#SP = Stocky_DB_2.Portfolio()
STU = Stocky_DB_2.Store_price()
STR= Stocky_DB_2.StockyDb()

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
        self.bot = telegram.Bot(token=self.Token)
        self.main()
        

    def start(self,update,context):
        user = update.message.from_user
        username = user.username
        update.message.reply_text(f"hello {data[username]}")

    def help(self,update,context):
        update.message.reply_text("""
        The following commands are available:
        /start
        /get_holdings
        /Recomndation
        /stock ticker
        /login""")

    def reco(self,update, context):
        buy, sell = STR.Recomodation()
        update.message.reply_text(f"Buy side: {buy.to_string},---------- Sell side: {sell.to_string}")


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
            #update.message.reply_text(f"we got you {data[username]},your holdings :-")
            for row in hold_df.iterrows():
                update.message.reply_text({row})
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
        disp.add_handler(telegram.ext.CommandHandler("Recomndation",self.reco))
        updater.start_polling()
        updater.idle()