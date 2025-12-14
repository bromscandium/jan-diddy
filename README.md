# Jan Diddy 2.0

**Jan Diddy 2.0** is a Telegram bot designed for group chats. It provides administrative tools, fun commands, and informational utilities, with a clear separation of concerns and a modular architecture.

## Project Structure

The project is organized to keep configuration, database access, handlers, business logic, and utilities clearly separated.

```
jan-diddy-2.0/
├── app/
│ ├── core/
│ │ ├── __init__.py
│ │ └── config.py        # Pydantic settings configuration
│ ├── db/
│ │ ├── __init__.py
│ │ └── postgres.py      # Tortoise ORM initialization
│ ├── handlers/
│ │ ├── __init__.py
│ │ ├── admin.py         # Admin commands
│ │ ├── chat.py          # Chat handlers
│ │ ├── events.py        # Event handlers (welcome, reactions)
│ │ ├── fun.py           # Fun commands
│ │ └── info.py          # Info commands
│ ├── models/
│ │ ├── __init__.py
│ │ ├── jokes.py         # Jokes model
│ │ ├── predictions.py   # Predictions model
│ │ └── warnings.py      # Warnings model
│ ├── services/
│ │ ├── __init__.py
│ │ ├── jokes.py         # Business logic for jokes
│ │ ├── predictions.py   # Business logic for predictions
│ │ └── warnings.py      # Business logic for warnings
│ ├── utils/
│ │ ├── __init__.py
│ │ └── decorators.py    # Rate limiting and chat decorators
│ └── main.py            # Application entry point
├── migrations/
│ └── models/
│ └── *.py               # Aerich migrations
├── .env                 # Environment variables
├── pyproject.toml
└── README.md
```

## Running the Bot

Make sure all dependencies are installed and environment variables are configured, then start the bot with:

```bash
python app/main.py
```
