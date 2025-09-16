import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "0"))
WEB_BASE_URL = os.getenv("WEB_BASE_URL", "").rstrip("/")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")

PUBLIC_MODE = os.getenv("PUBLIC_MODE", "off").lower() == "on"
