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
    


async def send_help(message: types.Message):
    await bot.send_message(message.from_user.id,
                 "Я могу показать:\n-) Общее количество мест"
                 "\n-) Количество бюджетных, платных, квотных и целевых мест"
                 "\n-) Минимальное количество баллов для поступающих на базе среднего профессионального или высшего образования"
                 "\n-) Минимальное количество баллов для вступительных испытаний (ЕГЭ)"
                 "\n-) Стоимость обучения\n\n"
                 "*В конце каждого вопроса указывайте название направления*",
                 reply_markup=None, parse_mode='Markdown')

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(send_help, commands=['help'])
    #dp.register_message_handler(send_question)