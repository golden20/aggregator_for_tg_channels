import os
from dotenv import load_dotenv
from pathlib import Path
# import pandas
import requests
import time

dotenv_path = Path('F:\\Vlad_F\\github_ds\\telegram_bot_project\\tg_vars.env')
load_dotenv(dotenv_path=dotenv_path)

TG_API_URL = os.getenv('TG_API_URL')
TG_TOKEN_ID = os.getenv('TG_TOKEN_ID')

TEXT_BOT = 'Great update!'

# print(TG_TOKEN_ID)

MAX_COUNTER = 100

offset = -2
counter = 0
chat_id: int


while counter < MAX_COUNTER:
    print('attempt =', counter)  #Чтобы видеть в консоли, что код живет
    updates = requests.get(f'{TG_API_URL}{TG_TOKEN_ID}/getUpdates?offset={offset + 1}').json()
    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            requests.get(f'{TG_API_URL}{TG_TOKEN_ID}/sendMessage?chat_id={chat_id}&text={TEXT_BOT}')

    time.sleep(1)
    counter += 1
