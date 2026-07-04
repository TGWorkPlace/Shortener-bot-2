import random
import string

from database import code_exists

# Uppercase letters + digits, e.g. A28UO (tweak if you also want lowercase)
CHARSET = string.ascii_uppercase + string.digits


async def generate_unique_code(length: int = 5) -> str:
    """Keep generating random codes until one that isn't already in the DB is found."""
    while True:
        code = "".join(random.choices(CHARSET, k=length))
        if not await code_exists(code):
            return code


def is_valid_url(text: str) -> bool:
    text = text.strip().lower()
    return text.startswith("http://") or text.startswith("https://")
