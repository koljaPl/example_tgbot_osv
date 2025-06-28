# Imports
import shortuuid
from typing import Optional
import aiosqlite
from pathlib import Path
from loguru import logger

# --- Database Path ---
DB_PATH = Path(__file__).parent / "bot_data.db"

# async def init_db():
#     """Инициализирует базу данных."""
#     async with aiosqlite.connect(DB_PATH) as db:
#         await db.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                 user_id INTEGER PRIMARY KEY,
#                 username TEXT,
#                 full_name TEXT,
#                 joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             )
#         """)
#         await db.commit()
#     logger.info("База данных инициализирована ✅")


# --- Initialization ---
# Самый дефолтный init_db | The most default init_db
async def init_db():
    """
    Initializes the database and creates all necessary tables
    if they don't exist. This is the single point of initialization.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        # Включаем поддержку внешних ключей | Enable foreign key support
        await db.execute("PRAGMA foreign_keys = ON;")

        # Создаем таблицу «users» | Create the 'users' table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                referral_count INTEGER DEFAULT 0
            )
        """)
        logger.info("Table 'users' initialized.")

        # Создает таблицу «referral_codes» для анонимных ссылок | Create the 'referral_codes' table for anonymous links
        await db.execute("""
            CREATE TABLE IF NOT EXISTS referral_codes (
                code TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)
        logger.info("Table 'referral_codes' initialized.")

        # Создает таблицу журнала «рефералы» | Create the 'referrals' log table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS referrals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                referrer_id INTEGER NOT NULL,
                referrer_username TEXT, 
                referral_id INTEGER NOT NULL UNIQUE,
                referral_username TEXT, 
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (referrer_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (referral_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)
        logger.info("Table 'referrals' initialized.")

        await db.commit()
    logger.info("База данных инициализирована ✅")

# --- User and Referral Management ---
# async def add_user(user_id: int, username: str, full_name: str):
#     """Добавляет пользователя в базу данных."""
#     async with aiosqlite.connect(DB_PATH) as db:
#         await db.execute("""
#             INSERT OR IGNORE INTO users (user_id, username, full_name)
#             VALUES (?, ?, ?)
#         """, (user_id, username, full_name))
#         await db.commit()
#     logger.info(f"Пользователь {username} ({user_id}) добавлен в базу ✅")

async def add_user_and_process_referral(
        user_id: int,
        username: str,
        full_name: str,
        referral_code: Optional[str] = None
):
    """
    Adds a new user to the database. If a valid referral code is provided,
    it processes the referral, linking the new user to their referrer.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        # Сначала проверяем, существует ли пользователь. | First, check if the user already exists.
        cursor = await db.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        existing_user = await cursor.fetchone()

        if existing_user:
            logger.info(f"User {username} ({user_id}) already exists.")
            return

        # Добавляем нового пользователя в таблицу «users» | Add the new user to the 'users' table
        await db.execute(
            "INSERT INTO users (user_id, username, full_name) VALUES (?, ?, ?)",
            (user_id, username, full_name)
        )
        logger.info(f"New user {username} ({user_id}) added to the database.")

        # Если код реферала не указан, все готово | If no referral code is provided, we're done.
        if not referral_code:
            await db.commit()
            return

        # --- Process the referral ---
        # 1. Find the referrer by their code | 1. Найдите реферера по его коду
        cursor = await db.execute(
            "SELECT user_id FROM referral_codes WHERE code = ?", (referral_code,)
        )
        referrer_row = await cursor.fetchone()

        if not referrer_row:
            logger.warning(f"Referral code '{referral_code}' is invalid or does not exist.")
            await db.commit()
            return

        referrer_id = referrer_row[0]

        # 2. Check that the user is not referring themselves | 2. Проверьте, что пользователь не ссылается на себя самого.
        if referrer_id == user_id:
            logger.warning(f"User {user_id} tried to refer themselves.")
            await db.commit()
            return

        # <<< NEW: Fetch the referrer's username from the user's table for logging
        # <<< НОВОЕ: Получить имя пользователя реферера из таблицы пользователей для регистрации в журнале
        cursor = await db.execute("SELECT username FROM users WHERE user_id = ?", (referrer_id,))
        referrer_username_row = await cursor.fetchone()
        # Provide a default value in case the username is missing for some reason
        referrer_username = referrer_username_row[0] if referrer_username_row else "unknown_referrer"

        # 3. Log the successful referral in the 'referrals' table | 3. Зарегистрируйте успешную регистрацию реферала в таблице 'referrals'.
        await db.execute(
            """INSERT INTO referrals (referrer_id, referrer_username, referral_id, referral_username)
               VALUES (?, ?, ?, ?)""",  # 4 columns, 4 placeholders | 4 столбца, 4 заполнителя
            (referrer_id, referrer_username, user_id, username)  # Correct variables in correct order | Правильные переменные в правильном порядке
        )
        logger.info(f"Referral logged: {referrer_username} ({referrer_id}) invited {username} ({user_id})")

        # 4. Increment the referrer's referral_count | 4. Увеличить значение referral_count реферера.
        await db.execute(
            "UPDATE users SET referral_count = referral_count + 1 WHERE user_id = ?",
            (referrer_id,)
        )
        logger.info(f"Referral count for user {referrer_id} incremented.")

        await db.commit()


async def get_user(user_id: int):
    """ Возвращает пользователя по ID | Returns the user by ID """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
            return await cursor.fetchone()


async def get_or_create_referral_code(user_id: int) -> str:
    """
    Gets the user's existing referral code. If it doesn't exist,     Получает существующий реферальный код пользователя. Если он не существует,
    creates a new unique, random code, saves it, and returns it.     создает новый уникальный случайный код, сохраняет его и возвращает.
    """

    async with aiosqlite.connect(DB_PATH) as db:
        # Check if a code already exists for this user | Проверяем, существует ли уже код для этого пользователя
        cursor = await db.execute("SELECT code FROM referral_codes WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()

        if row:
            return row[0]  # Return existing code |  Возврат существующего кода

        # If no code exists, generate a new one | Если код отсутствует, сгенерировать новый
        # Using shortuuid for clean, URL-safe codes | Использование shortuuid для создания чистых, безопасных для URL-адресов кодов
        new_code = shortuuid.uuid()[:8]  # e.g., 'q7aT9pWb'

        await db.execute("INSERT INTO referral_codes (code, user_id) VALUES (?, ?)", (new_code, user_id))
        await db.commit()
        logger.info(f"Generated new referral code '{new_code}' for user {user_id}.")
        return new_code
