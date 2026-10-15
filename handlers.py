from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    # Создаем клавиатуру вручную, чтобы точно знать, какие callback_data она шлет
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")]
    ])
    await message.answer("Привет! Это тест. Выбери язык:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("lang_"))
async def process_language(callback: CallbackQuery):
    # Извлекаем 'ru' или 'en' из 'lang_ru'
    lang = callback.data.split("_")[1]
    
    # Обязательно отвечаем на callback, чтобы у пользователя перестал крутиться значок загрузки
    await callback.answer(f"Язык {lang} выбран!")
    
    # Отправляем следующее сообщение
    await callback.message.answer(f"Отлично! Теперь просто напиши мне номер группы текстом (например: 03_ФИИТ_26_02)")
