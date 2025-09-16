import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

import bot.fdl  # import fdl command
import bot.public_mode  # public mode commands

async def start_bot():
    await dp.start_polling(bot)
