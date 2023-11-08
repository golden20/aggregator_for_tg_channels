import os
from dotenv import load_dotenv
from pathlib import Path

# import pandas
# import requests
# import time
# from pprint import pprint

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

dotenv_path = Path('F:\\Vlad_F\\github_ds\\telegram_bot_project\\tg_vars.env')
load_dotenv(dotenv_path=dotenv_path)

TG_API_URL = os.getenv('TG_API_URL')
TG_CATS_URL = os.getenv('TG_CATS_URL')
TG_TOKEN_ID = os.getenv('TG_TOKEN_ID')

# создание объекта бота и диспетчера
bot = Bot(token=TG_TOKEN_ID)
dp = Dispatcher()


# хендлер будет срабатывать на команду "/start"
@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь.')


# хендлер срабатывает на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь, и в ответ я напишу тебе твое сообщение :)')


# хендлер срабатывает на любые твои текстовые сообщения, кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)


if __name__ == 'main':
    dp.run_polling(bot)



# TEXT_BOT = 'Great update!'
# ERROR_TEXT_BOT = 'Здесь должна была быть картинка с котиком :('
# # print(TG_TOKEN_ID)
#
# MAX_COUNTER = 100
#
# offset = -2
# counter = 0
#
# chat_id: int
# cat_response: requests.Response
# cat_link: str
#
#
# while counter < MAX_COUNTER:
#     print('attempt =', counter)  #Чтобы видеть в консоли, что код живет
#     updates = requests.get(f'{TG_API_URL}{TG_TOKEN_ID}/getUpdates?offset={offset + 1}').json()
#     pprint(updates)
#     if updates['result']:
#         for result in updates['result']:
#             offset = result['update_id']
#             chat_id = result['message']['from']['id']
#             cat_response = requests.get(TG_CATS_URL)
#             if cat_response.status_code == 200:
#                 cat_link = cat_response.json()[0]['url']
#                 requests.get(f'{TG_API_URL}{TG_TOKEN_ID}/sendPhoto?chat_id={chat_id}&photo={cat_link}')
#             else:
#                 requests.get(f'{TG_API_URL}{TG_TOKEN_ID}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT_BOT}')
#             # requests.get(f'{TG_API_URL}{TG_TOKEN_ID}/sendMessage?chat_id={chat_id}&text={TEXT_BOT}')
#
#     time.sleep(1)
#     counter += 1
