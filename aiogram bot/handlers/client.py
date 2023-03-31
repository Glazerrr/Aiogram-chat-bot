from aiogram import types, Dispatcher
from create_bot import dp, bot
from pymystem3 import Mystem
import logging

logging.basicConfig(level=logging.INFO)

async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name}')
    await bot.send_message(message.from_user.id,
                 "Привет, я помогу тебе узнать информацию про выбранное направление, для этого задай вопрос в виде: <вопрос> <направление>\nЧтобы узнать о возможностях чат-бота введи /help",
                 reply_markup=None)
    await bot.send_message(message.from_user.id, f'{user_id}, {user_full_name}')


async def send_help(message: types.Message):
    await bot.send_message(message.from_user.id,
                 "Что я могу:\n-) Показать общее количество мест"
                 "\n-) Показать количество бюджетных, платных, квотных и целевых мест"
                 "\n-) Указать, какие документы нужны для поступления"
                 "\n-) Экзамены необходимые для поступления"
                 "\n-) Цена обучения"
                 "\n-) Минимальные баллы в прошлом году, проходные баллы"
                 "\n-) Какой был конкурс на место в прошлом году\n\n"
                 "*В конце каждого вопроса указывайте название направления*",
                 reply_markup=None, parse_mode='Markdown')



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(send_help, commands=['help'])
    #dp.register_message_handler(send_question)