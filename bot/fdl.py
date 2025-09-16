import asyncio
import secrets
import urllib.parse
from datetime import datetime
from mimetypes import guess_type
from aiogram import Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from pyrogram.enums import ChatMemberStatus
from bot import dp, SmartPyro
from config import LOG_CHANNEL_ID, WEB_BASE_URL
from .public_mode import CURRENT_PUBLIC
from config import ADMIN_ID

# ===== Helper Functions =====
async def send_message(chat_id, text, parse_mode=ParseMode.HTML, reply_markup=None, disable_web_page_preview=False):
    bot = Bot.get_current()
    return await bot.send_message(chat_id, text, parse_mode=parse_mode, reply_markup=reply_markup, disable_web_page_preview=disable_web_page_preview)

class SmartButtons:
    def __init__(self):
        self.buttons = []
    def button(self, text, url):
        self.buttons.append({"text": text, "url": url})
    def build_menu(self, b_cols=2):
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        keyboard = []
        row = []
        for i, btn in enumerate(self.buttons, start=1):
            row.append(InlineKeyboardButton(text=btn["text"], url=btn["url"]))
            if i % b_cols == 0:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

# ===== File Utils =====
async def get_file_properties(message: Message):
    file_name, file_size, mime_type = None, 0, None
    if message.document:
        file_name = message.document.file_name
        file_size = message.document.file_size
        mime_type = message.document.mime_type
    elif message.video:
        file_name = getattr(message.video, 'file_name', None)
        file_size = message.video.file_size
        mime_type = message.video.mime_type
    elif message.audio:
        file_name = getattr(message.audio, 'file_name', None)
        file_size = message.audio.file_size
        mime_type = message.audio.mime_type
    elif message.photo:
        file_size = message.photo[-1].file_size
        mime_type = "image/jpeg"
        file_name = f"photo-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
    elif message.video_note:
        file_size = message.video_note.file_size
        mime_type = "video/mp4"
        file_name = f"video-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
    if not mime_type:
        mime_type = guess_type(file_name)[0] or "application/octet-stream"
    return file_name, file_size, mime_type

async def format_file_size(file_size: int) -> str:
    if file_size < 1024 * 1024:
        return f"{file_size/1024:.2f} KB"
    elif file_size < 1024 * 1024 * 1024:
        return f"{file_size/(1024*1024):.2f} MB"
    return f"{file_size/(1024*1024*1024):.2f} GB"

# ===== Main Handler =====
async def handle_file_download(message: Message, bot: Bot):
    if not message.reply_to_message:
        return await message.reply("<b>Please reply to a media file</b>", parse_mode=ParseMode.HTML)
    reply_message = message.reply_to_message
    if not (reply_message.document or reply_message.video or reply_message.photo or reply_message.audio or reply_message.video_note):
        return await message.reply("<b>Reply must be a valid media file</b>", parse_mode=ParseMode.HTML)

    processing_msg = await message.reply("<b>Processing...</b>", parse_mode=ParseMode.HTML)
    code = secrets.token_urlsafe(6)[:6]
    file_name, file_size, mime_type = await get_file_properties(reply_message)

    # forward to log channel
    sent = await reply_message.forward(LOG_CHANNEL_ID)
    file_id = sent.message_id
    await SmartPyro.copy_message(
        chat_id=LOG_CHANNEL_ID,
        from_chat_id=LOG_CHANNEL_ID,
        message_id=file_id,
        caption=code
    )

    quoted_code = urllib.parse.quote(code)
    base_url = WEB_BASE_URL.rstrip('/')
    download_link = f"{base_url}/dl/{file_id}?code={quoted_code}"
    stream_link = f"{base_url}/stream/{file_id}?code={quoted_code}" if mime_type.startswith('video') else None

    buttons = SmartButtons()
    buttons.button("🚀 Download Link", download_link)
    if stream_link:
        buttons.button("🖥️ Stream Link", stream_link)
    keyboard = buttons.build_menu()

    response = (
        f"<b>✨ Your Links are Ready! ✨</b>\n\n"
        f"<code>{file_name}</code>\n"
        f"<b>📂 Size:</b> {await format_file_size(file_size)}\n\n"
        f"<b>🚀 Download:</b> <a href='{download_link}'>{download_link}</a>\n"
    )
    if stream_link:
        response += f"<b>🖥️ Stream:</b> <a href='{stream_link}'>{stream_link}</a>\n"
    await processing_msg.edit_text(response, parse_mode=ParseMode.HTML, reply_markup=keyboard, disable_web_page_preview=True)

# ===== Command Binding =====
@dp.message(Command("fdl"))
async def fdl_command(message: Message, bot: Bot):
    from bot.public_mode import CURRENT_PUBLIC
    if not CURRENT_PUBLIC and message.from_user.id != ADMIN_ID:
        return await message.reply("🚫 Private mode. Only admin can use this.")
    await handle_file_download(message, bot)
