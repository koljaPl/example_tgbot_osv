# Imports:
import logging
import sys
import os
import asyncio

# Logger
from loguru import logger

# Все импорты aiogram | All aiogram imports
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# Импорты из моих файлов | Imports from my files
from src.handlers.main_handlers import router

# Импорты бд | DB Imports
from src.database.db import init_db as sqlite_init_db

# Реферальная система
from src.referral_system import rfs_main


# Проверка конфигурационных файлов | Checking configuration files
try:
    from config.config import MAIN_BOT_TOKEN   # Убедись, что этот путь правильный | Make sure this path is the right one
except ImportError:
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"  # Заглушка, если config не найден | Plug if config not found
    print("ПРЕДУПРЕЖДЕНИЕ: Не найден файл config.py. Используется токен-заглушка. Бот не запустится корректно.\n"
          "WARNING: The config.py file was not found. A stub token is being used. The bot will not start correctly.")
    if TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("ПОЖАЛУЙСТА, УКАЖИТЕ ВАШ TELEGRAM_BOT_TOKEN В КОДЕ ИЛИ В ФАЙЛЕ КОНФИГУРАЦИИ.\n"
              "PLEASE SPECIFY YOUR TELEGRAM_BOT_TOKEN IN THE CODE OR IN THE CONFIGURATION FILE.")
        exit()


# --- Логирование --- Logging ---
# Настройка логирования | Configuring logging
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Перехватываем стандартные логи и передаём их в loguru | Capture standard logs and pass them to loguru
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())

def setup_logging():
    # Удаляем стандартный обработчик, чтобы избежать дублирования | Remove the default handler to avoid duplication.
    logger.remove()

    # Формат логов | Log format
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level>| "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    # Логи в консоль | Log format
    logger.add(
        sys.stdout,
        format=log_format,
        level="INFO",
        colorize=True,
    )

    # Логи в файл с ротацией | Logs to a file with rotation
    log_dir = "src/logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger.add(
        f"{log_dir}/bot_{{time:YYYY-MM-DD}}.log",
        format=log_format,
        level="DEBUG",
        rotation="1 day",  # Ротация логов каждый день | Rotating logs every day
        retention="7 days",  # Хранить логи 7 дней | Keep logs for 7 days
        compression="zip",  # Архивировать старые логи | Archive old logs
        encoding="utf-8",
    )
    logging.basicConfig(handlers=[InterceptHandler()], level=0)


# База данных | Database
async def init_db():
    logger.info("Инициализация базы данных...")
    logger.info("Initializing database...")
    await sqlite_init_db()


# --- Запуск бота --- Launching the bot
async def main():
    # Инициализация логирования | Initializing logging
    setup_logging()

    await init_db()

    # --- Общая инициализация --- General initialization ---

    bot = Bot(token=MAIN_BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    storage = MemoryStorage()  # Для продакшена лучше RedisStorage или другой персистентный
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    # DELETED: The old referral system initializations are gone
    # УДАЛЕНО: Старые инициализации системы рефералов удалены.
    # init_referral_db()
    # dp.include_router(rfs_main.router)

    logger.info("Запускаем...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен через кнопку выключения")
        logger.info("The bot was stopped using the shutdown button")
    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}", exc_info=True)
        logger.critical(f"Critical error: {e}", exc_info=True)


