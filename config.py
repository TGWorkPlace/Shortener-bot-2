import os

# Telegram API credentials (from https://my.telegram.org)
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Comma separated Telegram user IDs allowed to use the bot
ADMIN_IDS = [
    int(x) for x in os.environ.get("ADMIN_IDS", "").split(",") if x.strip().isdigit()
]

# MongoDB
MONGO_URI = os.environ.get("MONGO_URI", "")
DB_NAME = os.environ.get("DB_NAME", "url_shortener")

# Public base URL of your deployed backend, e.g. https://domain.app
BASE_URL = os.environ.get("BASE_URL", "").rstrip("/")

# Web server
PORT = int(os.environ.get("PORT", "8080"))

# Length of the random short code, e.g. A28UO -> 5
CODE_LENGTH = int(os.environ.get("CODE_LENGTH", "5"))
