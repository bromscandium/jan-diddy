# Jan Diddy

Version 6.0.0

Asynchronous Telegram bot built with Python 3.14, python-telegram-bot, and Tortoise ORM. It combines classic group management (moderation, info, fun commands) with an AI persona that passively listens to the chat and occasionally replies in character via a separate LLM engine.

## Architecture

The application is split into vertical slices by domain, mirroring the two database schemas.

```
app/
├── main.py                 thin entrypoint — BotApplication().run()
├── core/                   shared kernel
│   ├── application.py      BotApplication: build, lifecycle, error handling, run
│   ├── bot.py              BotSettings   (telegram, webhook, admin, timezone)
│   ├── db.py               DBSettings    (DATABASE_URL, url)
│   ├── llm.py              LLMSettings + TriggerConfig (persona engine + triggers)
│   ├── postgres.py         Tortoise config + connect/close (migrations on startup)
│   ├── redis.py            RedisSettings + Redis client
│   ├── http.py             shared aiohttp session
│   └── logger.py           loguru
├── community/              classic bot (schema "bot")
│   ├── models.py           BotModel base + Jokes, Predictions, Warnings
│   ├── services/           jokes, predictions, warnings, weather
│   └── handlers/           admin, chat, events, fun, info
├── persona/                AI persona (schema "llm")
│   ├── models.py           LLMModel base + Messages, BotReplies, SuccessfulDialogs
│   ├── services/           state, triggers, persona_client, scoring, history
│   └── handlers/           listener, reactions
└── handlers/__init__.py    setup_handlers() — wires both slices
```

The persona engine (`../jan-diddy-llm`) is a separate service reached over HTTP; the
bot never loads the model itself.

## Features

- Administrative Tools: ban, unban, mute, unmute, and a multi-level warning system with automated temporary restrictions.
- Targeted Content Filter: homoglyph/leetspeak normalization filter for users in the banned registry.
- Information Services: academic schedules, rules, Moodle links, semester progress.
- Entertainment: OpenWeatherMap weather, random jokes, probability predictions.
- AI Persona: passive listener that reconstructs recent chat context, probabilistically decides to reply, and generates an in-character reply via the LLM engine. Successful replies (reactions / laughter keywords) are recorded for future fine-tuning.

## Technical Stack

- Python 3.14, Poetry 2.4.1
- PostgreSQL (async, asyncpg) via Tortoise ORM + Aerich migrations
- Redis (hot state: message buffer, counters, scoring window)
- Pydantic Settings, loguru, python-telegram-bot 22.5
- Docker, Railway.com

## Configuration

Defined in `.env` locally (see `.env.sample`) or the Railway dashboard.

- BOT_TOKEN: Telegram Bot API token.
- WEATHER_API_KEY: OpenWeatherMap API key.
- DATABASE_URL: PostgreSQL connection string (`postgresql://user:pass@host:port/db`).
- REDIS_URL: Redis connection string.
- CHAT_ID / ADMIN_CHAT_ID: main group and admin/log group IDs.
- ADMIN_IDS / BANNED_BY_ID: privileged users and filter targets.
- SEMESTER_START (YYYY-MM-DD), TIMEZONE (default Europe/London).
- DEBUG: `true` uses the aggressive DEBUG trigger profile (reply every 2 messages).
- PERSONA_ENGINE_URL / PERSONA_ENGINE_SECRET / PERSONA_ENGINE_TIMEOUT: LLM engine endpoint and shared secret.
- WEBHOOK_DOMAIN / WEBHOOK_PATH / WEBHOOK_SECRET / PORT: webhook mode; if WEBHOOK_DOMAIN is empty the bot falls back to long polling.

## Local Development via Docker

```
cp .env.sample .env      # fill in the values
docker compose up --build
```

Brings up `db`, `redis`, and the `bot`. The persona engine runs separately (see
`../jan-diddy-llm`); the compose bot reaches it via `host.docker.internal`.

## Deployment on Railway.com

1. Provision PostgreSQL and Redis.
2. `railway link` and `railway up` (or link the GitHub repo).
3. Set the Configuration variables; DATABASE_URL is linked from the PostgreSQL service.
4. The `postgresql://` → `postgres://` scheme conversion is handled automatically.

## Database Migrations

Managed via Aerich.

```
poetry run aerich migrate     # create a migration after model changes
poetry run aerich upgrade     # apply migrations
```

Migrations are applied automatically on startup (`connect_db`) and in the Docker
`CMD`, so a deploy needs no manual step.

## Tests

```
poetry run pytest
```
