# src/referral_system/rfs_db.py

from src.database.db import DB_PATH
import aiosqlite

async def get_referral_count(user_id: int) -> int:
    """
    Возвращает количество рефералов у пользователя | Returns the number of referrals for the user
    """
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM referrals WHERE referrer_id = ?", (user_id,)
        )
        result = await cursor.fetchone()
        return result[0] if result else 0

