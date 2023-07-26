import requests, json, os
from dotenv import load_dotenv

load_dotenv()

"""
TelegramBot Instance to send message to user
"""
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID_SELF')

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Error code: {response.status_code}")
        
def get_chat_id():
    url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
    response = requests.get(url)
    data = response.json()
    if 'result' in data and data['result']:
        chat_id = data['result'][0]['message']['chat']['id']
        return chat_id
    else:
        return None