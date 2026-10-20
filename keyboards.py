from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from locales import t

def main_menu_kb(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang, "today")), KeyboardButton(text=t(lang, "tomorrow"))],
            [KeyboardButton(text=t(lang, "week")), KeyboardButton(text=t(lang, "next_week_btn"))],
            [KeyboardButton(text=t(lang, "custom_date")), KeyboardButton(text=t(lang, "settings_btn"))],
            [KeyboardButton(text=t(lang, "groups_btn")), KeyboardButton(text=t(lang, "help_btn"))],
            [KeyboardButton(text="🆕 Что нового?"), KeyboardButton(text=t(lang, "donate_btn"))],
        ],
        resize_keyboard=True,
    )

def language_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇧 English", callback_data="lang_en")],
    ])

def action_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "groups_btn"), callback_data="action_group")],
        [InlineKeyboardButton(text=t(lang, "language_btn"), callback_data="action_language")],
        [InlineKeyboardButton(text=t(lang, "help_btn"), callback_data="action_menu")],
    ])from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from locales import t


def main_menu_kb(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang, "today")), KeyboardButton(text=t(lang, "tomorrow"))],
            [KeyboardButton(text=t(lang, "week")), KeyboardButton(text=t(lang, "next_week_btn"))],  # <-- Замени "custom_date" на "next_week_btn"
            [KeyboardButton(text=t(lang, "custom_date")), KeyboardButton(text=t(lang, "settings_btn"))],
            [KeyboardButton(text=t(lang, "groups_btn")), KeyboardButton(text=t(lang, "help_btn"))],
            [KeyboardButton(text="🆕 Что нового?"), KeyboardButton(text=t(lang, "settings_btn"))],
            [KeyboardButton(text=t(lang, "donate_btn"))],
        ],
        resize_keyboard=True,
    )


def language_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
    ])


def action_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "groups_btn"), callback_data="action_group")],
        [InlineKeyboardButton(text=t(lang, "language_btn"), callback_data="action_language")],
        [InlineKeyboardButton(text=t(lang, "help_btn"), callback_data="action_menu")],
    ])
