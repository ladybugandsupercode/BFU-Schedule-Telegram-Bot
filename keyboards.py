from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from locales import t


def main_menu_kb(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang, "today")), KeyboardButton(text=t(lang, "tomorrow"))],
            [KeyboardButton(text=t(lang, "week")), KeyboardButton(text=t(lang, "custom_date"))],
            [KeyboardButton(text=t(lang, "language_btn"))],
            [KeyboardButton(text=t(lang, "settings_btn"))],
        ],
        resize_keyboard=True,
    )


def language_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
    ])