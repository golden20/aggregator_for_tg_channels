from aiogram import Bot, Dispatcher, F
from aiogram.filters import BaseFilter
from aiogram.types import Message

import os
from dotenv import load_dotenv
from pathlib import Path


dotenv_path = Path('/\\tg_vars.env')
load_dotenv(dotenv_path=dotenv_path)

TG_API_URL = os.getenv('TG_API_URL')
TG_CATS_URL = os.getenv('TG_CATS_URL')
TG_TOKEN_ID = os.getenv('TG_TOKEN_ID')

# создание объекта бота и диспетчера
bot = Bot(token=TG_TOKEN_ID)
dp = Dispatcher()


# список админов
admin_ids: list[int] = [497500344]


# кастомный фильтр на проверку пользователей, являются ли они админами
class AdminFilter(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        # передаем список с целыми числами (id пользователей)
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


# Этот фильтр будет проверять наличие неотрицательных чисел
# в сообщении от пользователя, и передавать в хэндлер их список
class NumbersInMessage(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, list[int]]:
        numbers = []
        # Разрезаем сообщение по пробелам, нормализуем каждую часть, удаляя
        # лишние знаки препинания и невидимые символы, проверяем на то, что
        # в таких словах только цифры, приводим к целым числам
        # и добавляем их в список
        for word in message.text.split():
            normalized_word = word.replace('.', '').replace(',', '').strip()
            if normalized_word.isdigit():
                numbers.append(int(normalized_word))
        # Если в списке есть числа - возвращаем словарь со списком чисел по ключу 'numbers'
        if numbers:
            return {'numbers': numbers}
        return False


# Этот хэндлер будет срабатывать, если сообщение пользователя
# начинается с фразы "найди числа" и в нем есть числа
@dp.message(F.text.lower().startswith('найди числа'), NumbersInMessage())
# Помимо объекта типа Message, принимаем в хэндлер список чисел из фильтра
async def process_if_numbers(message: Message, numbers: list[int]):
    await message.answer(text=f'Нашел: {", ".join(str(num) for num in numbers)}')


# Этот хэндлер будет срабатывать, если сообщение пользователя
# начинается с фразы "найди числа", но в нем нет чисел
@dp.message(F.text.lower().startswith('найди числа'))
async def process_if_not_numbers(message: Message):
    await message.answer(text='Не нашел что-то :(')


# # хендлер на получение апдейтов от админа
# @dp.message(AdminFilter(admin_ids))
# async def answer_if_admins_update(message: Message):
#     # return None
#     await message.answer(text='You are admin')


# # хендлер на получение апдейтов не от админа
# @dp.message()
# async def answer_if_not_admins_update(message: Message):
#     # return None
#     await message.answer(text='You are not admin')


if __name__ == '__main__':
    dp.run_polling(bot)

