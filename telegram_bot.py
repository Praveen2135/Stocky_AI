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

    def stock(update, context):
        price = get_live_price(context.args[0])
        price= round(price,2)
        update.message.reply_text(f"Stock price: {price}")

    def login(self,update,context):
        update.message.reply_text("Please give user name")
        user=(update.message)
        update.message.reply_text(user)

    def get_holdings(update, context):
        user = update.message.from_user
        username = user.username
        print(username)
        #Get the user data
        if username in data.keys():
            update.message.reply_text(f"we got you {data[username]}")
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