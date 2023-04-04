from aiogram import Bot, Dispatcher
import os

TOKEN = os.getenv('TOKEN')
bot = Bot(token = TOKEN)
dp = Dispatcher(bot)
