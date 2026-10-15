import json
import time
import logging
from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram import types

log = logging.getLogger(__name__)

from config import CACHE_TTL_MINUTES
from database import (
    set_user_group, get_user_group, get_cached_schedule, save_cached_schedule,
    set_user_language, get_user_language
)
from keyboards import main_menu_kb, language_kb, action_kb
from parser import fetch_schedule, get_today, get_tomorrow, get_week_dates
from locales import t

logger = logging.getLogger(__name__)
router = Router()


class Register(StatesGroup):
    waiting_group = State()
    waiting_language = State()
    waiting_custom_date = State()
    waiting_action = State()


def format_day(date_key: str, lessons: list, lang: str) -> str:
    if not lessons:
        return f"<b>📅 {date_key}</b>\n\n{t(lang, 'no_classes')}"

    day_name = datetime.strptime(date_key, "%Y-%m-%d").strftime("%A, %d.%m")
    lines = [f"<b>📅 {day_name}</b>\n"]
    for l in lessons:
        lines.append(
            f"⏰ <b>{l['time']}</b>\n"
            f"📘 <b>{l['subject']}</b>\n"
            f"👨‍🏫 {l['teacher']}\n"
            f"🏫 {l['room']}\n"
        )
    return "\n".join(lines)


async def get_schedule_for_user(telegram_id: int, force_refresh: bool = False) -> dict | None:
    if not force_refresh:
        cached = await get_cached_schedule(telegram_id)
        if cached and cached[1]:
            age = int(time.time()) - cached[1]
            if age < CACHE_TTL_MINUTES * 60 and cached[0]:
                return json.loads(cached[0])

    group = await get_user_group(telegram_id)
    if not group:
        return None

    data = await fetch_schedule(group)
    if data is not None:
        await save_cached_schedule(telegram_id, json.dumps(data), int(time.time()))
    return data


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    group = await get_user_group(message.from_user.id)
    lang = await get_user_language(message.from_user.id)
    
    if group:
        await message.answer(
            t(lang, "welcome_back", group=group),
            reply_markup=action_kb(lang),
            parse_mode="HTML"
        )
    else:
        await state.set_state(Register.waiting_language)
        await message.answer(
            t(lang, "welcome"),
            reply_markup=language_kb(),
            parse_mode="HTML"
        )


@router.message(Command("reset"))
async def cmd_reset(message: Message, state: FSMContext):
    await set_user_group(message.from_user.id, "")
    await set_user_language(message.from_user.id, "ru")
    await state.clear()
    await state.set_state(Register.waiting_language)
    await message.answer(
        t("ru", "reset_success"),
        reply_markup=language_kb(),
        parse_mode="HTML"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    lang = await get_user_language(message.from_user.id)
    await message.answer(
        t(lang, "help_message"),
        parse_mode="HTML"
    )


@router.message(Command("groups"))
async def cmd_groups(message: Message):
    lang = await get_user_language(message.from_user.id)
    groups_text = (
        "📋 <b>Список специальностей БФУ</b>\n\n"
        "🎓 <b>Бакалавриат/Специалитет (03_):</b>\n"
        "• 03_ФИИТ_26_02 — Информационные системы и технологии\n"
        "• 03_СТР_26_1 — Строительство\n"
        "• 03_АРХ_26 — Архитектура\n"
        "• 03_МАШ_26 — Машиностроение\n"
        "• 03_ТТП_26 — Технология транспортных процессов\n"
        "• 03_СЕРВ_26_упс — Сервис\n"
        "• 03_СОЦ_26 — Социология\n"
        "• 03_ПОЛ_26 — Политология\n"
        "• 03_МО_26 — Международные отношения\n"
        "• 03_ИСТ_26_1 — История\n"
        "• 03_ФК_26 — Физическая культура\n\n"
        "🎓 <b>Магистратура (04_):</b>\n"
        "• 04_МАТЕМ_26 — Математика\n"
        "• 04_ФИЗ_26 — Физика\n"
        "• 04_ХИМ_26 — Химия\n\n"
        "🎓 <b>Колледжи (02_):</b>\n"
        "• 02_арх_26_9 — Архитектура\n"
        "• 02_ИСП_25_9 — Информационные системы и программирование\n"
        "• 02_РУПО_26_9 — Разработка и управление ПО\n\n"
        "💡 <b>Полный список очень большой!</b>\n"
        "📌 Введи свою группу в формате: <code>03_ФИИТ_26_02</code>\n\n"
        "🆘 <b>Не нашёл свою группу?</b>\n"
        "Напишите в поддержку: @your_username"
    )
    await message.answer(groups_text, parse_mode="HTML")


@router.callback_query(F.data.startswith("lang_"))
async def process_language(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split("_")[1]
    await set_user_language(callback.from_user.id, lang)
    await state.set_state(Register.waiting_action)
    
    await callback.answer()
    await callback.message.answer(
        t(lang, "after_language"),
        reply_markup=action_kb(lang),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "action_group")
async def action_choose_group(callback: CallbackQuery, state: FSMContext):
    lang = await get_user_language(callback.from_user.id)
    await state.set_state(Register.waiting_group)
    await callback.answer()
    await callback.message.answer(
        t(lang, "enter_group"),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "action_language")
async def action_change_language(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Register.waiting_language)
    await callback.answer()
    await callback.message.answer(
        t("ru", "choose_lang"),
        reply_markup=language_kb(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "action_menu")
async def action_show_menu(callback: CallbackQuery, state: FSMContext):
    lang = await get_user_language(callback.from_user.id)
    group = await get_user_group(callback.from_user.id)
    
    if not group:
        await state.set_state(Register.waiting_group)
        await callback.answer()
        await callback.message.answer(
            t(lang, "enter_group"),
            parse_mode="HTML"
        )
        return
    
    await state.clear()
    await callback.answer()
    await callback.message.answer(
        t(lang, "welcome_back", group=group),
        reply_markup=main_menu_kb(lang),
        parse_mode="HTML"
    )


@router.message(Register.waiting_group)
async def process_group(message: Message, state: FSMContext):
    lang = await get_user_language(message.from_user.id)
    group = message.text.strip()

    menu_buttons = [
        t("ru", "today"), t("en", "today"),
        t("ru", "tomorrow"), t("en", "tomorrow"),
        t("ru", "week"), t("en", "week"),
        t("ru", "custom_date"), t("en", "custom_date"),
        t("ru", "settings_btn"), t("en", "settings_btn"),
        t("ru", "language_btn"), t("en", "language_btn"),
        t("ru", "groups_btn"), t("en", "groups_btn"),
        t("ru", "help_btn"), t("en", "help_btn")
    ]
    
    if group in menu_buttons:
        await message.answer(t(lang, "enter_group"), parse_mode="HTML")
        return

    if len(group) < 3:
        await message.answer(t(lang, "group_invalid"), parse_mode="HTML")
        return

    data = await fetch_schedule(group)
    if data is None:
        await message.answer(t(lang, "group_not_found"), parse_mode="HTML")
        return

    await set_user_group(message.from_user.id, group)
    await state.clear()
    await message.answer(
        t(lang, "group_saved", group=group),
        reply_markup=main_menu_kb(lang),
        parse_mode="HTML"
    )


@router.message(F.text.in_([t("ru", "today"), t("en", "today")]))
async def show_today(message: Message):
    lang = await get_user_language(message.from_user.id)
    await show_day(message, get_today(), lang)


@router.message(F.text.in_([t("ru", "tomorrow"), t("en", "tomorrow")]))
async def show_tomorrow(message: Message):
    lang = await get_user_language(message.from_user.id)
    await show_day(message, get_tomorrow(), lang)


async def show_day(message: Message, date_key: str, lang: str):
    schedule = await get_schedule_for_user(message.from_user.id)
    if schedule is None:
        await message.answer(t(lang, "error_schedule"), parse_mode="HTML")
        return
    lessons = schedule.get(date_key, [])
    await message.answer(format_day(date_key, lessons, lang), parse_mode="HTML")


@router.message(F.text.in_([t("ru", "week"), t("en", "week")]))
async def show_week(message: Message):
    lang = await get_user_language(message.from_user.id)
    schedule = await get_schedule_for_user(message.from_user.id)
    if schedule is None:
        await message.answer(t(lang, "error_schedule"), parse_mode="HTML")
        return
    days = get_week_dates()
    parts = [format_day(d, schedule.get(d, []), lang) for d in days]
    full = "\n\n".join(parts)

    if len(full) <= 4000:
        await message.answer(full, parse_mode="HTML")
    else:
        for d in days:
            await message.answer(format_day(d, schedule.get(d, []), lang), parse_mode="HTML")


@router.message(F.text.in_([t("ru", "custom_date"), t("en", "custom_date")]))
async def ask_custom_date(message: Message, state: FSMContext):
    lang = await get_user_language(message.from_user.id)
    await message.answer(t(lang, "enter_date"), parse_mode="HTML")
    await state.set_state(Register.waiting_custom_date)


@router.message(Register.waiting_custom_date)
async def process_custom_date(message: Message, state: FSMContext):
    lang = await get_user_language(message.from_user.id)
    try:
        date_obj = datetime.strptime(message.text.strip(), "%d.%m.%Y")
        date_key = date_obj.strftime("%Y-%m-%d")
        await show_day(message, date_key, lang)
        await state.clear()
    except ValueError:
        await message.answer(t(lang, "date_invalid"), parse_mode="HTML")


@router.message(F.text.in_([t("ru", "settings_btn"), t("en", "settings_btn")]))
async def settings(message: Message, state: FSMContext):
    lang = await get_user_language(message.from_user.id)
    group = await get_user_group(message.from_user.id)
    await message.answer(
        t(lang, "settings", group=group or "—"),
        parse_mode="HTML"
    )
    await state.set_state(Register.waiting_group)


@router.message(F.text.in_([t("ru", "language_btn"), t("en", "language_btn")]))
async def change_language(message: Message, state: FSMContext):
    await state.set_state(Register.waiting_language)
    await message.answer(
        t("ru", "choose_lang"),
        reply_markup=language_kb(),
        parse_mode="HTML"
    )


@router.message(F.text.in_([t("ru", "groups_btn"), t("en", "groups_btn")]))
async def show_groups(message: Message):
    await cmd_groups(message)


@router.message(F.text.in_([t("ru", "help_btn"), t("en", "help_btn")]))
async def show_help(message: Message):
    await cmd_help(message)

@router.callback_query()
async def fallback_callback(call: types.CallbackQuery, state: FSMContext):
    log.warning("Необработанная кнопка: data=%r, state=%r",
                call.data, await state.get_state())
    await call.answer("Кнопка устарела, нажми /start", show_alert=True)

@router.message()
async def fallback_message(message: types.Message, state: FSMContext):
    log.warning("Необработанное сообщение: text=%r, state=%r",
                message.text, await state.get_state())
    await message.answer("Не понял 🤔 Нажми /start, чтобы вернуться в меню")
