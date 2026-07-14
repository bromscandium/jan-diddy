# CLAUDE.md

Guidance for working in this repository.

## What this is

`jan-diddy` — an async Telegram bot (Python 3.14, python-telegram-bot 22.5, Tortoise ORM + Aerich, Redis, Poetry). It pairs classic group management with an AI persona that talks to a separate LLM engine over HTTP.

Companion repo: `../jan-diddy-llm` (the persona engine — FastAPI + Ollama). The bot reaches it via `PERSONA_ENGINE_URL` and authenticates with `PERSONA_ENGINE_SECRET` (header `X-Engine-Secret`). The bot never loads the model.

## Structure — vertical slices by domain

- `app/community/` — classic bot, DB schema `bot` (jokes, predictions, warnings + admin/info/fun/events/chat).
- `app/persona/` — AI persona, DB schema `llm`. Folder-per-domain / file-per-responsibility: `handlers/` (thin listener + reactions dispatch), `orchestrator/` (reply pipeline — `flow` + `addressing`/`payload`/`ingest`/`formatting`/`media`), `client/` (HTTP to engine — `base._request` helper + `reply`/`vision`/`health`), `scoring/` (`rules` pure + `keys` + `flywheel` redis/DB). Leaf single-responsibility modules stay flat: `state`, `history`, `profiles`, `triggers`, `rendering`, `lexicon`, `models`. Rule: make a folder only when a unit has real internal seams; otherwise one file.
- `app/core/` — shared kernel. Settings are split per domain: `bot.py` (`bot_settings`), `db.py` (`db_settings`), `llm.py` (`llm_settings` + `TriggerConfig`), `redis.py` (`redis_settings` + client). `application.py` holds `BotApplication` (build/lifecycle/run); `main.py` just calls `BotApplication().run()`.
- `app/handlers/__init__.py` — `setup_handlers()` wires both slices.

Each slice has one `models.py` with an abstract base (`BotModel` / `LLMModel`) that carries the shared `schema` + common fields; concrete models subclass it and set only their `table`.

## Conventions

- No comments in code — none. Prefer self-explanatory code and type hints. Where a decorated function body would be empty, use `...`.
- Config is read via the split settings objects (`bot_settings`, `db_settings`, `llm_settings`, `redis_settings`) — there is no single `settings`.
- Repeated handler shapes are factored into decorators (see `random_reply` in `community/handlers/fun.py`). Per-user rate limits key on `func.__name__`, so keep handler names distinct (`functools.wraps`).
- Migrations run automatically on startup via `connect_db` (Aerich `upgrade`); no manual step on deploy.

## Commands

- Tests: `poetry run pytest` (SQLite in-memory; conftest nulls schemas since SQLite has none).
- Migrate: `poetry run aerich migrate` then `poetry run aerich upgrade`.
- Local stack: `docker compose up --build` (db + redis + bot; engine runs separately).

## Trigger behaviour

`core/llm.py` has `PROD` and `DEBUG` `TriggerConfig` profiles; `DEBUG=true` in `.env` selects DEBUG (replies every 2 messages, no cooldown). Webhook vs polling is chosen by whether `WEBHOOK_DOMAIN` is set.
