import os

from aiohttp import web

from database import get_link, increment_click

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "redirect.html")

with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    REDIRECT_TEMPLATE = f.read()


async def health_handler(request: web.Request):
    return web.Response(text="OK")


async def redirect_handler(request: web.Request):
    code = request.match_info.get("code")

    link = await get_link(code)
    if not link:
        return web.Response(
            text="<h2 style='font-family:sans-serif;text-align:center;margin-top:20%;'>"
            "404 &mdash; Link not found</h2>",
            content_type="text/html",
            status=404,
        )

    await increment_click(code)

    original_url = link["original_url"]
    html = REDIRECT_TEMPLATE.replace("{{URL}}", original_url)
    return web.Response(text=html, content_type="text/html")


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/", health_handler)
    app.router.add_get("/{code}", redirect_handler)
    return app
