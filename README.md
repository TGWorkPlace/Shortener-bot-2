# URL Shortener (bit.ly style) — Pyrogram bot + aiohttp backend

Admin-only Telegram bot that turns any link into `https://domain.app/{CODE}`,
backed by MongoDB, with a green-themed HTML redirect page as the public-facing side.

## How it works

- **Bot (`bot.py`)**: Only users listed in `ADMIN_IDS` can talk to it. Send it
  any `http(s)://` link and it replies with a shortened link like
  `https://domain.app/A28UO`.
- **Storage (`database.py`)**: Each short code + original URL pair is stored
  in a MongoDB `links` collection (`code`, `original_url`, `admin_id`,
  `clicks`, `created_at`).
- **Web server (`web_server.py`)**: aiohttp app. `GET /{code}` looks the code
  up in Mongo and serves `templates/redirect.html`, which:
  - shows a white background page
  - shows green text counting down "Redirecting in 5 seconds..."
  - redirects via JS after 5s (and via `<meta http-equiv="refresh">` as a
    backup)
  - always shows a green capsule-shaped "Open Link" button in case the
    automatic redirect doesn't fire.
- **`main.py`**: runs the web server and the bot together in one process —
  this is what you deploy.

## Setup

1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and fill in:
   - `API_ID` / `API_HASH` — from https://my.telegram.org
   - `BOT_TOKEN` — from @BotFather
   - `ADMIN_IDS` — comma separated Telegram user IDs allowed to use the bot
   - `MONGO_URI` / `DB_NAME` — your MongoDB connection
   - `BASE_URL` — the public domain this backend will be reachable at
     (e.g. `https://domain.app`), used only to build the short link text
     shown to the admin
3. Run: `python main.py`

On Koyeb (or any host), just make sure:
- The service listens on `$PORT` (already handled via `config.PORT`,
  defaults to 8080) and that port is exposed publicly as your domain.
- All the env vars above are set in the service's environment settings.

## Notes / things you may want to tweak

- Short codes are 5 characters, uppercase letters + digits (e.g. `A28UO`),
  controlled by `CODE_LENGTH` in `.env`. Uniqueness is checked against Mongo
  before saving, with a unique index on `code` as a safety net.
- `is_valid_url` only requires the text to start with `http://` or
  `https://` — tighten this if you want stricter validation.
- Only private messages are handled; group chats are ignored by design
  since this is meant to be an admin-only tool.
- `clicks` is tracked per link if you want to add a "stats" command later.
