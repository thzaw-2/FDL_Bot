from aiogram import Dispatcher
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

dp = Dispatcher()

# Pyrogram client (bot account)
SmartPyro = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)
