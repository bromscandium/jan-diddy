# Jan Diddy

Asynchronous Telegram bot built with Python 3.14, python-telegram-bot, and Tortoise ORM. Designed for group management, information distribution, and automated moderation.

## Features

- Administrative Tools: Full suite of moderation commands including ban, unban, mute, unmute, and a multi-level warning system with automated temporary restrictions.
- Targeted Content Filter: Aggressive word filter using homoglyph normalization and noise removal, specifically targeting users listed in the banned registry.
- Information Services: Automated distribution of academic schedules, rules, Moodle links, and semester progress tracking.
- Entertainment Modules: Weather integration via OpenWeatherMap, random joke generation, and probability predictions.
- Robust Architecture: Powered by Tortoise ORM with Aerich migrations, Pydantic Settings for configuration, and automated rate limiting.

## Technical Stack

- Language: Python 3.14
- Dependency Management: Poetry 2.4.1
- Database: PostgreSQL (Async via asyncpg)
- ORM: Tortoise ORM
- Deployment: Docker, Railway.com

## Configuration

The application requires the following environment variables. These should be defined in a .env file for local development or within the Railway dashboard for production.

- BOT_TOKEN: Telegram Bot API token.
- WEATHER_API_KEY: OpenWeatherMap API key.
- DATABASE_URL: Full PostgreSQL connection string (postgresql://user:pass@host:port/db).
- CHAT_ID: Main group chat ID.
- ADMIN_CHAT_ID: Group ID for error logs and bot notifications.
- ADMIN_IDS: List of user IDs with full administrative access.
- GRANT_ADMIN_IDS: List of user IDs with limited administrative permissions.
- SEMESTER_START: Date in YYYY-MM-DD format.
- TIMEZONE: Regional timezone (default: Europe/London).
- BANNED_BY_ID: List of user IDs subject to the targeted word filter.

## Local Development via Docker

Ensure Docker and Docker Compose are installed on your system.

1. Clone the repository and navigate to the directory.
2. Create a .env file based on .env.sample.
3. Execute the following command to build and start the services:
   
   docker compose up --build

The services will be initialized in an isolated network. The database port is not exposed to the host machine for security purposes.

## Deployment on Railway.com

This project is optimized for deployment on Railway using the provided Dockerfile.

1. Create a new project on Railway.
2. Provision a PostgreSQL instance.
3. Link your repository or use the Railway CLI:
   
   railway link
   railway up

4. Configuration on Railway:
   - Ensure the DATABASE_URL variable is correctly linked from your PostgreSQL service.
   - Add all remaining variables from the Configuration section to the bot service.
   - The bot will automatically handle the postgresql:// to postgres:// scheme conversion required by Tortoise ORM.

## Database Migrations

Database schema changes are managed via Aerich.

- Initializing a new database:
  poetry run aerich init-db

- Creating a new migration after model changes:
  poetry run aerich migrate

- Applying migrations:
  poetry run aerich upgrade

Note: On Railway and within Docker Compose, migrations are applied automatically during the container startup process.

## Moderation Policy

The bot implements a strict content policy for designated users. Messages containing prohibited substrings (including variations using leetspeak or homoglyphs) are automatically deleted without further notification to maintain group decorum.
