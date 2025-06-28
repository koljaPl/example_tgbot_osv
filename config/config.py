# Imports
from dotenv import load_dotenv
import os

# Грузим из .env файла данные | Loading data from the .env file
load_dotenv()

# Все токены и ваши данные используются в анонимном формате | All tokens and your data are used in an anonymous format
MAIN_BOT_TOKEN = os.getenv("MAIN_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
BOT_USERNAME = os.getenv("BOT_USERNAME")

# Неиспользованные импорты из dotenv | Unused imports from dotenv
# ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")
# SECOND_ADMIN_ID = int(os.getenv("SECOND_ADMIN_ID", 0))
# SECOND_ADMIN_USERNAME = os.getenv("SECOND_ADMIN_USERNAME")