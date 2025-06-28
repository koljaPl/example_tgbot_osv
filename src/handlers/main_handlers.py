# Imports
import os
from aiogram import Router, F, types
from aiogram.filters import Command  # Убран CommandObject
from aiogram.filters import CommandStart
from aiogram.filters.command import CommandObject
from aiogram.types import FSInputFile
from aiogram.types import InputMediaPhoto
from aiogram.types import (Message)

# Imports from my files | Импорт из моих файлов
from config.texts_config import info_text, bot_username
from scripts.some_scripts.get_bitcoin_price_script import get_bitcoin_price
# Imports from database | Импорты из дата баз
from src.database.db import add_user_and_process_referral, get_or_create_referral_code
from src.keyboards.inline_keyboards import get_main_inline_keyboard
from src.keyboards.main_keyboards import get_main_reply_keyboard
from src.referral_system.rfs_main import get_referral_count

router = Router()

# FIXED: Changed CommandStart(deep_link=True) to CommandStart() to catch all /start commands
# ИСПРАВЛЕНО: Изменено CommandStart(deep_link=True) на CommandStart(), чтобы перехватить все команды /startImports из моих файлов.
@router.message(CommandStart())
async def start_message(message: types.Message, command: CommandObject):
    """
        Handles all /start commands, registering new users and processing referrals.
        Обрабатывает все команды /start, регистрирует новых пользователей и обрабатывает рефералов.
    """
    user = message.from_user

    referral_code = command.args if command.args else None

    user_id = user.id
    username = user.username or "unknown"
    full_name = user.full_name or "No Name"

    # This single function handles all the complex logic | Эта единственная функция обрабатывает всю сложную логику.
    await add_user_and_process_referral(
        user_id=user.id,
        username=user.username or "unknown",
        full_name=user.full_name or "No Name",
        referral_code=referral_code
    )

    await message.answer(
        f"👋 Привет! Ты запустил бота.",
        reply_markup=get_main_reply_keyboard()
    )



@router.message(Command("info"))
async def info_message(message: types.Message):
    await message.answer(info_text
                         , reply_markup=get_main_inline_keyboard() # <-- Показываю как работают keyboard | Showing how keyboards work
                         )

@router.message(Command("menu"))
async def menu_handler(message: types.Message):
    await message.answer(
        "Выберите действие:",
        reply_markup=get_main_inline_keyboard()
    )

@router.message(Command("bitcoin"))
@router.message(F.text.lower() == "bitcoin")
async def handle_bitcoin_request(message: types.Message):
    await message.answer(get_bitcoin_price())

@router.message(Command("photo"))
async def send_photo(message: types.Message):
    photo_text = "Hello My Friend!"
    photo_path = os.path.join("src", "pictures", "main_pictures", "1.png")  # путь к изображению (или URL) в папке pictures например | image path (or URL)
                                                                                                    # in the pictures folder e.g.,
    # Если фото у тебя локально на диске | If you have the photo locally on your disk
    if os.path.exists(photo_path):
        photo = FSInputFile(photo_path)
        await message.answer_photo(photo=photo, caption=photo_text)
    else:
        await message.answer("❌ Файл не найден. Проверь путь к изображению.")

    # Если ты хочешь отправить фото по URL (например, с интернета) | If you want to send a photo via URL (e.g., from the Internet)
    # await message.answer_photo(photo="https://example.com/image.jpg", caption=info_text)


@router.message(Command("ManyPhoto"))
async def send_gallery(message: types.Message):
    gallery_text = "Hello My Friend!"

    files = [
        FSInputFile("src/pictures/products_pictures/1.png"),
        FSInputFile("src/pictures/products_pictures/2.png"),
    ]
    media = [
        InputMediaPhoto(media=files[0], caption="📸 Галерея фото:\n\n👉 Это описание будет только у первого фото"),
        InputMediaPhoto(media=files[1]),
    ]

    await message.answer_media_group(media)

@router.message(Command('HowManyReferrals'))
@router.message(F.text == 'Сколько у меня рефералов?')
async def HowManyRefferals(message: Message):
    user_id = message.from_user.id

    count = await get_referral_count(user_id)

    await message.answer(f"👥 У тебя {count} реферал(ов).")


@router.message(Command('referral'))
@router.message(F.text == "Реферальная ссылка")
async def my_ref_link(message: Message):
    """
    Generates and provides the user with their unique, anonymous referral link.
    Генерирует и предоставляет пользователю его уникальную анонимную реферальную ссылку.
    """
    # 1. Get the unique code from the database
    user_id = message.from_user.id
    code = await get_or_create_referral_code(user_id)

    # 2. Generate the link
    link = f"https://t.me/{bot_username}?start={code}"

    await message.answer(f"Вот твоя реферальная ссылка:\n`{link}`", parse_mode="Markdown")  # Using backticks for easy copy-paste