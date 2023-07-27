import requests, json, os
from dotenv import load_dotenv     
from telegram import Update, Chat
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext


"""
Environment Variables
"""
load_dotenv()
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id_ck = os.getenv('TELEGRAM_CHAT_ID_SELF') # default chat id
chat_id_dev = os.getenv('TELEGRAM_CHAT_ID_DEV')

"""
TelegramBot Instance to send message to user
"""
telegram_bot = Updater(bot_token, use_context=True)
telegram_bot_dispatcher = telegram_bot.dispatcher



"""
Function to send message to message to specified chat_id

@param: 
    - ChatId of chat to send message (Chat with CK by default if not specified)
    - Message to be sent
@return: N/A if success, prints error message if failed to send message
"""
def send_message(message, chat_id=chat_id_ck):
    telegram_bot.bot.send_message(chat_id=chat_id, text=message)



""""
Function to send current chatID to user
"""
def send_chat_id(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    
    context.bot.send_message(chat_id=chat_id, text=f"Chat ID: {chat_id}")
    print(f"Chat ID: {chat_id}")



"""
Command Handlers
"""
send_chat_id = CommandHandler('id', send_chat_id)
telegram_bot_dispatcher.add_handler(send_chat_id)



"""
Module initializer
"""

def main():
    telegram_bot.start_polling()
    print("SpotiSense Telegram Bot is now live!")
    telegram_bot.idle()

if __name__ == "__main__":
    main()
