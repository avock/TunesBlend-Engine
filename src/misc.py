import requests, json, os
from dotenv import load_dotenv

load_dotenv()

"""
TelegramBot Instance to send message to user
"""
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID_SELF')

"""
Function to send message to message to specified chat_id

@param: 
    - Telegram Bot's botToken to send said message (SpotiSenseBot by default if not specified)
    - ChatId of chat to send message (Chat with CK by default if not specified)
    - Message to be sent
@return: N/A if success, prints error message if failed to send message
"""
def send_telegram_message(message, bot_token=bot_token, chat_id=chat_id):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        pass
    else:
        print(f"Failed to send telegram message. Error code: {response.status_code}")
       
"""
Function to obtain list of chat_id of the telegram bot
""" 
def get_chat_id():
    url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
    response = requests.get(url)
    data = response.json()
    if 'result' in data and data['result']:
        chat_id = data['result'][0]['message']['chat']['id']
        return chat_id
    else:
        return None