from aiogram.filters import Command
from aiogram.types import Message
from config import ADMIN_ID, PUBLIC_MODE
from bot import dp

CURRENT_PUBLIC = PUBLIC_MODE  # start state from env


@dp.message(Command("public"))
async def toggle_public(message: Message):
    global CURRENT_PUBLIC
    if message.from_user.id != ADMIN_ID:
        return await message.reply("❌ You are not authorized.")
    
    args = message.text.split()
    if len(args) < 2:
        return await message.reply("Usage: /public on | off")
    
    if args[1].lower() == "on":
        CURRENT_PUBLIC = True
        await message.reply("✅ Public mode enabled")
    elif args[1].lower() == "off":
        CURRENT_PUBLIC = False
        await message.reply("🔒 Public mode disabled")
    else:
        await message.reply("Usage: /public on | off")
