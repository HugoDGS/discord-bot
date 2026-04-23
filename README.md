# Discord Bot

A modular Discord bot with moderation, utility, reminders and fun commands.

## Stack

- Python 3.11+
- discord.py 2.x (prefix commands + listeners)
- SQLite (persistent reminders and custom responses)
- python-dotenv

## Features

| Category | Commands |
|---|---|
| **Moderation** | `kick`, `ban`, `unban`, `timeout`, `clear` |
| **Utility** | `ping`, `serverinfo`, `userinfo`, `avatar`, `help` |
| **Fun** | `poll`, `roll`, `coin` |
| **Reminders** | `remind`, `reminders`, `cancelreminder` |

Welcome messages are sent automatically when a new member joins.

## Setup

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your bot token:

```
DISCORD_TOKEN=your_bot_token_here
PREFIX=!
```

Create a bot at [discord.com/developers](https://discord.com/developers/applications), enable **Server Members Intent** and **Message Content Intent**, then invite the bot with `bot` and `applications.commands` scopes.

```bash
python bot/main.py
```

## Command reference

### Reminders

```
!remind 30m Stand up meeting
!remind 2h Check the deployment
!reminders
!cancelreminder 3
```

### Poll

```
!poll "Favourite language?" Python JavaScript Go
```

Reactions are added automatically. Up to 10 options.
