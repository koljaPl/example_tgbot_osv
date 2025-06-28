from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_main_reply_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="📄 Помощь")
    builder.button(text="⚙️ Настройки")
    builder.button(text="❓ Задать вопрос")
    builder.adjust(2)  # по 2 кнопки в строке | 2 buttons per row

    return builder.as_markup(resize_keyboard=True, input_field_placeholder="Выберите действие")
