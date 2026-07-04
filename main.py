import asyncio
import logging
import sys

from aiohttp import web
from pyrogram import idle
from pyrogram.errors import FloodWait

import config
from bot import bot
from database import init_indexes
from web_server import create_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("main")


async def start_web_server():
    app = create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", config.PORT)
    await site.start()
    logger.info(f"[web] Redirect server running on port {config.PORT}")


async def start_bot_resilient():
    """Retry bot.start() instead of letting one hiccup crash the whole process
    (and take the entire container down with it)."""
    while True:
        try:
            await bot.start()
            return
        except FloodWait as e:
            wait_time = int(e.value) + 10
            logger.warning(f"FLOOD_WAIT during login. Sleeping {wait_time}s...")
            await asyncio.sleep(wait_time)
        except Exception:
            logger.exception("Critical startup error, retrying in 15s...")
            await asyncio.sleep(15)


async def main():
    if not config.ADMIN_IDS:
        logger.warning("No ADMIN_IDS configured — nobody will be able to use the bot.")

    try:
        await init_indexes()
        logger.info("MongoDB index ready.")
    except Exception:
        logger.exception(
            "Failed to reach MongoDB / create index. Check MONGO_URI. "
            "The bot will still start, but link storage will fail."
        )

    await start_web_server()

    await start_bot_resilient()
    me = await bot.get_me()
    logger.info(f"[bot] Pyrogram bot started as @{me.username}. Listening for messages...")

    await idle()

    await bot.stop()


if __name__ == "__main__":
    asyncio.run(main())
