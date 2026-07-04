import logging
import traceback

from pyrogram import Client, filters
from pyrogram.types import Message

import config
from database import save_link
from utils import generate_unique_code, is_valid_url

logger = logging.getLogger("shortener_bot")

bot = Client(
    "url_shortener_bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
)


def is_admin(user_id: int) -> bool:
    return user_id in config.ADMIN_IDS


@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    try:
        if not is_admin(message.from_user.id):
            await message.reply_text("🚫 You are not authorized to use this bot.")
            return

        await message.reply_text(
            "👋 **URL Shortener Bot**\n\n"
            "Send me any link (starting with http:// or https://) and I'll "
            "shorten it for you.\n\n"
            f"Short links look like: `{config.BASE_URL}/A28UO`"
        )
    except Exception:
        logger.error("Error in start_handler:\n%s", traceback.format_exc())
        try:
            await message.reply_text("⚠️ Something went wrong handling /start. Check the logs.")
        except Exception:
            pass


@bot.on_message(filters.private & filters.text & ~filters.command("start"))
async def link_handler(client: Client, message: Message):
    try:
        if not is_admin(message.from_user.id):
            await message.reply_text("🚫 You are not authorized to use this bot.")
            return

        url = message.text.strip()

        if not is_valid_url(url):
            await message.reply_text(
                "⚠️ That doesn't look like a valid URL. It must start with "
                "`http://` or `https://`."
            )
            return

        code = await generate_unique_code(config.CODE_LENGTH)
        await save_link(code, url, message.from_user.id)

        short_url = f"{config.BASE_URL}/{code}"

        await message.reply_text(
            "✅ **Link shortened!**\n\n"
            f"🔗 Original: {url}\n"
            f"✂️ Short: `{short_url}`",
            disable_web_page_preview=True,
        )
    except Exception:
        logger.error("Error in link_handler:\n%s", traceback.format_exc())
        try:
            await message.reply_text(
                "⚠️ Something went wrong shortening that link (likely a database issue). "
                "Check the bot logs."
            )
        except Exception:
            pass
