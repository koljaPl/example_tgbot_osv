from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="ℹ️ Информация", callback_data="info")
    builder.button(text="💬 Связаться", callback_data="contact")
    builder.button(text="❌ Закрыть", callback_data="close")
    builder.adjust(2)  # по 2 кнопки в строке

    return builder.as_markup()
