import telegram
from telegram.ext import *

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
        /get_stock_price
        /get_portfolio
        /login""")

    def login(self,update,context):
        update.message.reply_text("Please give user name")
        user=(update.message)
        update.message.reply_text(user)

    def main(self):
        updater = telegram.ext.Updater(self.Token,use_context=True)
        disp = updater.dispatcher
        disp.add_handler(telegram.ext.CommandHandler("start",self.start))
        disp.add_handler(telegram.ext.CommandHandler("help",self.help))
        updater.start_polling()
        updater.idle()