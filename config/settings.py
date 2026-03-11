import os
from dotenv import load_dotenv
from pathlib import Path

# Базова директорія проєкту (дві папки вище від config/settings.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# Завантаження .env
load_dotenv(BASE_DIR / ".env")

# Змінні оточення
DATABASE_URL = os.getenv("DATABASE_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Перевірка на None
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL не знайдено у .env! Перевір файл .env")
if BOT_TOKEN is None:
    raise ValueError("BOT_TOKEN не знайдено у .env! Перевір файл .env")