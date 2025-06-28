# Imports
from dataclasses import dataclass, field
from typing import Literal
import uuid
from datetime import datetime

# Example class of a product | Пример класса продукта
@dataclass
class GameAccount:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    game_name: str = "Unknown Game"
    platform: Literal["PC", "PS4", "PS5", "Xbox", "Mobile"] = "PC"
    login: str = ""
    password: str = ""
    price_usd: float = 0.0
    region: str = "Global"
    level: int = 1
    skins: list[str] = field(default_factory=list)
    email_access: bool = False  # Есть ли доступ к почте |  Is there access to mail
    is_sold: bool = False
    added_at: datetime = field(default_factory=datetime.utcnow)

    def display_summary(self) -> str:
        """Краткое описание для Telegram-сообщения | Brief description for Telegram message"""
        return (
            f"🎮 *{self.game_name}* ({self.platform})\n"
            f"📦 Уровень/LVL: {self.level}\n"
            f"📍 Регион/Region: {self.region}\n"
            f"💰 Цена/Price: ${self.price_usd:.2f}\n"
            f"📧 Почта/Mail: {'✅' if self.email_access else '❌'}\n"
            f"🆔 ID: `{self.id}`\n"
        )

    def mark_as_sold(self):
        """Помечает аккаунт как проданный | Mark account as sold"""
        self.is_sold = True

    def to_dict(self) -> dict:
        """
           Преобразует аккаунт в словарь (например, для записи в JSON или БД)
           Converts an account into a dictionary (e.g., for writing to JSON or a database)
        """
        return {
            "id": self.id,
            "game_name": self.game_name,
            "platform": self.platform,
            "login": self.login,
            "password": self.password,
            "price_usd": self.price_usd,
            "region": self.region,
            "level": self.level,
            "skins": self.skins,
            "email_access": self.email_access,
            "is_sold": self.is_sold,
            "added_at": self.added_at.isoformat()
        }