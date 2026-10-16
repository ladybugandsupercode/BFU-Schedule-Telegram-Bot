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
from dedupe import DedupeMiddleware
from version import BOT_VERSION, CHANGELOG


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

router.message.outer_middleware(DedupeMiddleware())

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
    
    if group:
        # Если группа уже есть, показываем обычное приветствие на выбранном языке
        lang = await get_user_language(message.from_user.id)
        await message.answer(
            t(lang, "welcome_back", group=group),
            reply_markup=main_menu_kb(lang),
            parse_mode="HTML"
        )
    else:
        # Если группы нет (новый пользователь), показываем двуязычное приветствие
        await state.set_state(Register.waiting_language)
        await message.answer(
            t("ru", "welcome_bilingual"), # Берём из ru, так как там уже два языка
            reply_markup=language_kb(),
            parse_mode="HTML"
        )


@router.message(Command("reset"))
async def cmd_reset(message: Message, state: FSMContext):
    await set_user_group(message.from_user.id, "")
    await set_user_language(message.from_user.id, "ru")
    await state.clear()
    await state.set_state(Register.waiting_language)
    
    # Теперь это ОДНО чистое сообщение без лишнего текста
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
    await message.answer(
        t(lang, "groups_message"),
        parse_mode="HTML"
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
        t(lang, "groups_text"),
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


# === КОМАНДА ДЛЯ АДМИНА: МАССОВАЯ РАССЫЛКА ===
ADMIN_TELEGRAM_ID = 5638577090  # Твой telegram_id

@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message):
    """Отправляет сообщение всем пользователям (только для админа)."""
    if message.from_user.id != ADMIN_TELEGRAM_ID:
        await message.answer("⛔ У вас нет прав для этой команды.")
        return
    
    # Проверяем, есть ли текст после команды
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer(
            "📢 <b>Использование:</b>\n"
            "<code>/broadcast Текст сообщения</code>\n\n"
            "Пример:\n"
            "<code>/broadcast 🎉 Добавлена новая функция!</code>",
            parse_mode="HTML"
        )
        return
    
    broadcast_text = args[1]
    
    # Получаем всех пользователей
    from database import get_all_user_ids
    user_ids = await get_all_user_ids()
    
    await message.answer(f"📤 Начинаю рассылку {len(user_ids)} пользователям...")
    
    success_count = 0
    fail_count = 0
    
    for user_id in user_ids:
        try:
            await message.bot.send_message(user_id, broadcast_text, parse_mode="HTML")
            success_count += 1
        except Exception as e:
            logger.warning(f"Не удалось отправить сообщение пользователю {user_id}: {e}")
            fail_count += 1
    
    await message.answer(
        f"✅ Рассылка завершена!\n"
        f"📤 Успешно: {success_count}\n"
        f"❌ Ошибок: {fail_count}"
    )

# === АВТОМАТИЧЕСКОЕ УВЕДОМЛЕНИЕ ПРИ ОБНОВЛЕНИИ ===
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    group = await get_user_group(message.from_user.id)
    
    # Проверяем, нужно ли показать уведомление об обновлении
    from database import get_user_notified_version, set_user_notified_version
    notified_version = await get_user_notified_version(message.from_user.id)
    
    if notified_version != BOT_VERSION and BOT_VERSION in CHANGELOG:
        # Показываем информацию о новой версии
        await message.answer(
            CHANGELOG[BOT_VERSION],
            parse_mode="HTML"
        )
        # Отмечаем, что пользователь уведомлен
        await set_user_notified_version(message.from_user.id, BOT_VERSION)
    
    if group:
        lang = await get_user_language(message.from_user.id)
        await message.answer(
            t(lang, "welcome_back", group=group),
            reply_markup=main_menu_kb(lang),
            parse_mode="HTML"
        )
    else:
        await state.set_state(Register.waiting_language)
        await message.answer(
            t("ru", "welcome_bilingual"),
            reply_markup=language_kb(),
            parse_mode="HTML"
        )

# === КОМАНДА /CHANGELOG ===
@router.message(Command("changelog"))
async def cmd_changelog(message: Message):
    """Показывает историю изменений."""
    lang = await get_user_language(message.from_user.id)
    
    changelog_text = "📋 <b>История изменений:</b>\n\n"
    for version, description in CHANGELOG.items():
        changelog_text += f"{description}\n\n"
    
    await message.answer(changelog_text, parse_mode="HTML")



@router.message(F.text == "🆕 Что нового?")
async def show_changelog(message: Message):
    await cmd_changelog(message)
