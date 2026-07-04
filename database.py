from datetime import datetime, timezone

import motor.motor_asyncio

import config

# serverSelectionTimeoutMS makes Mongo failures raise quickly (5s) instead of
# hanging silently and making the bot look "active but unresponsive".
client = motor.motor_asyncio.AsyncIOMotorClient(
    config.MONGO_URI,
    serverSelectionTimeoutMS=5000,
)
db = client[config.DB_NAME]
links = db["links"]


async def init_indexes():
    """Call once on startup to make sure lookups by code are unique/fast."""
    await links.create_index("code", unique=True)


async def code_exists(code: str) -> bool:
    return await links.find_one({"code": code}) is not None


async def save_link(code: str, original_url: str, admin_id: int) -> dict:
    doc = {
        "code": code,
        "original_url": original_url,
        "admin_id": admin_id,
        "clicks": 0,
        "created_at": datetime.now(timezone.utc),
    }
    await links.insert_one(doc)
    return doc


async def get_link(code: str):
    return await links.find_one({"code": code})


async def increment_click(code: str):
    await links.update_one({"code": code}, {"$inc": {"clicks": 1}})
