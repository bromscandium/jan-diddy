# Jan Diddy 2.0

Modernized Telegram Bot for student group management, built with high performance and reliability in mind.

## Tech Stack

- Python 3.14+
- python-telegram-bot v22.5 (Async)
- Tortoise ORM (Async ORM)
- PostgreSQL (Database)
- Aerich (Migrations)
- Loguru (Advanced Logging)
- Poetry (Dependency Management)
- Pytest + Polyfactory (Automated Testing)
- Ruff (Linting & Formatting)

## Project Structure

- app/core/: Configuration, logging, and global HTTP sessions.
- app/db/: Database connection and ORM settings.
- app/handlers/: Bot command handlers and event logic.
- app/models/: Tortoise ORM database models.
- app/services/: Business logic separated from handlers.
- app/utils/: Decorators (admin access, rate limits) and helpers.
- migrations/: Database migration history.
- tests/: Automated test suite.

## Local Development

### 1. Requirements
- Python 3.14
- Poetry
- PostgreSQL

### 2. Installation
```bash
poetry install
```

### 3. Configuration
Copy .env.sample to .env and fill in your credentials:
```bash
cp .env.sample .env
```

### 4. Database Migrations
Initialize or upgrade the database schema:
```bash
poetry run aerich upgrade
```

### 5. Running the Bot
```bash
poetry run python -m app.main
```

## Testing & Quality

### Run Tests
```bash
poetry run pytest
```

### Linting
```bash
poetry run ruff check .
```

## Docker & Production (Railway.com)

The project is production-ready with a Dockerfile.

### Build and Run locally:
```bash
docker build -t jan-diddy .
docker run --env-file .env jan-diddy
```

## Production Features:
- Automated Migrations: Runs aerich upgrade automatically on startup.
- Graceful Shutdown: Ensures DB and HTTP connections close cleanly.
- Global Error Handling: Reports critical errors to the admin group.
- Timezone Support: Configurable via TIMEZONE env variable.
