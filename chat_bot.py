import random
import sys
#from neuralintents import GenericAssistant
import telegram
from telegram.ext import *


def greetings():
    responses=["Hello Sir","Hey","Hi...!"]
    reply= random.choice(responses)
    print(reply)

def bye():
    print('Good Bye...!')
    sys.exit()

mappings = {'greetings':greetings,
            'bye':bye}

assistant = GenericAssistant('intents.json',mappings)

assistant.train_model()
assistant.save_model()

def chat_bot():
    while True:
        msg=input()
        assistant.request(msg)

Token='5900892098:AAEHsv03l9Ow7LOc80re1ESq-sMu6VOvCXs'

def start(update,context):
  update.message.reply_text("hello praveen")

updater = telegram.ext.Updater(Token,use_context = True)

disp = updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler("start",start))

updater.start_polling()
updater.idle()