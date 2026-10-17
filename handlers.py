# handlers.py

import asyncio
import html
import logging
from datetime import date, datetime, timedelta
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from database import (
    set_user_group, get_user_group,
    set_user_language, get_user_language,
    get_all_user_ids, get_user_notified_version, set_user_notified_version,
)
from dedupe import DedupeMiddleware
from keyboards import main_menu_kb, language_kb, action_kb
from locales import t, WEEKDAYS
from parser import fetch_schedule, today_date, get_week_dates
from version import BOT_VERSION, CHANGELOG, changelog_text

logger = logging.getLogger(__name__)

router = Router()
router.message.outer_middleware(DedupeMiddleware())

# telegram_id админа (только он может делать /broadcast)
ADMIN_TELEGRAM_ID = 5638577090

# Допустимые годы для ввода даты
MIN_YEAR, MAX_YEAR = 2000, 2100


class Register(StatesGroup):
    waiting_group = State()
    waiting_language = State()
    waiting_custom_date = State()
    waiting_action = State()


def esc(value) -> str:
    """Экранирует символы <, > и &, чтобы Telegram не ломался на HTML-разметке."""
    return html.escape(str(value), quote=False)


# ============================================================
#  ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================

def format_day(date_key: str, lessons: list, lang: str) -> str:
    """Форматирует один день. Дата снаружи, все пары внутри красивой цитаты."""
    d = datetime.strptime(date_key, "%Y-%m-%d")
    weekdays = WEEKDAYS.get(lang, WEEKDAYS["ru"])
    
    # Дата СНАРУЖИ цитаты
    header = f"<b>📅 {weekdays[d.weekday()]}, {d.strftime('%d.%m.%Y')}</b>"

    if not lessons:
        return f"{header}\n\n{t(lang, 'no_classes')}"

    # Собираем строки для цитаты
    quote_lines = []
    for l in lessons:
        # Кабинет жирным для мгновенного считывания
        room_bold = f"<b>{esc(l['room'])}</b>"
        
        # Если номер пары есть, добавляем его красиво
        num_prefix = f"🔢 <b>{esc(l['lesson_num'])} пара</b> | " if l['lesson_num'] else ""
        
        line = (
            f"⏰ {esc(l['time'])}\n"
            f"{num_prefix}📘 {esc(l['subject'])}\n"
            f"👨‍🏫 {esc(l['teacher'])}\n"
            f"🏫 {room_bold}"
        )
        quote_lines.append(line)

    # Объединяем все пары дня в один блок цитаты
    quote_text = "\n\n".join(quote_lines)
    
    return f"{header}\n\n<blockquote>{quote_text}</blockquote>"


async def get_schedule_for_user(telegram_id: int, day: date | None = None) -> dict | None:
    """Расписание на неделю, в которую попадает день `day` (по умолчанию текущая неделя).
    Кэш (на 30 минут) живёт внутри parser.fetch_schedule."""
    group = await get_user_group(telegram_id)
    if not group:
        return None
    return await fetch_schedule(group, day)


def parse_user_date(text: str) -> date | None:
    """Разбирает дату, введённую пользователем.
    Понимает: 15.10.2026, 15.10.26, 15.10 (текущий год), 15/10/2026, 15-10-2026, 2026-10-15."""
    cleaned = (text or "").strip().replace("/", ".").replace("-", ".").replace(",", ".")
    parts = cleaned.split(".")
    if len(parts) == 2:  # ДД.ММ, значит, берём текущий год
        cleaned = f"{cleaned}.{today_date().year}"

    for fmt in ("%d.%m.%Y", "%d.%m.%y", "%Y.%m.%d"):
        try:
            d = datetime.strptime(cleaned, fmt).date()
        except ValueError:
            continue
        if MIN_YEAR <= d.year <= MAX_YEAR:
            return d
    return None


async def show_day(message: Message, day: date, lang: str):
    schedule = await get_schedule_for_user(message.from_user.id, day)
    if schedule is None:
        await message.answer(t(lang, "error_schedule"), parse_mode="HTML")
        return
    lessons = schedule.get(day.isoformat(), [])
    await message.answer(format_day(day.isoformat(), lessons, lang), parse_mode="HTML")


# ============================================================
#  КОМАНДЫ (/start, /reset, /help, /groups, /changelog, /broadcast)
# ============================================================

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    
    group = await get_user_group(message.from_user.id)
    lang = await get_user_language(message.from_user.id)

    # Уведомление о новой версии (try/except: если что-то пойдёт не так, /start всё равно сработает)
    try:
        notified_version = await get_user_notified_version(message.from_user.id)
        if notified_version != BOT_VERSION and BOT_VERSION in CHANGELOG:
            if group:
                # Существующему пользователю показываем, что нового, на его языке
                await message.answer(changelog_text(BOT_VERSION, lang), parse_mode="HTML")
            # Новому пользователю (ещё без группы) просто молча отмечаем версию
            await set_user_notified_version(message.from_user.id, BOT_VERSION)
    except Exception as e:
        logger.error("Ошибка уведомления об обновлении: %r", e)

    if group:
        await message.answer(
            t(lang, "welcome_back", group=esc(group)),
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


@router.message(Command("reset"))
async def cmd_reset(message: Message, state: FSMContext):
    await set_user_group(message.from_user.id, "")
    await set_user_language(message.from_user.id, "ru")
    await state.clear()
    await state.set_state(Register.waiting_language)

    await message.answer(
        t("ru", "reset_success"),  # этот текст сразу на двух языках
        reply_markup=language_kb(),
        parse_mode="HTML"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    lang = await get_user_language(message.from_user.id)
    await message.answer(t(lang, "help_message"), parse_mode="HTML")


@router.message(Command("groups"))
async def cmd_groups(message: Message):
    lang = await get_user_language(message.from_user.id)
    await message.answer(t(lang, "groups_message"), parse_mode="HTML")


@router.message(Command("changelog"))
async def cmd_changelog(message: Message):
    """Показывает историю изменений (новые версии сверху) на языке пользователя."""
    lang = await get_user_language(message.from_user.id)
    parts = [t(lang, "changelog_header")]
    for version in reversed(list(CHANGELOG.keys())):
        parts.append(changelog_text(version, lang))
    await message.answer("\n\n".join(parts), parse_mode="HTML")


@router.message(F.text.in_([t("ru", "changelog_btn"), t("en", "changelog_btn")]))
async def show_changelog(message: Message):
    await cmd_changelog(message)


@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message):
    """Рассылка всем пользователям (только для админа).
    Формат: /broadcast Текст  или  /broadcast Русский текст ||| English text"""
    admin_lang = await get_user_language(message.from_user.id)

    if message.from_user.id != ADMIN_TELEGRAM_ID:
        await message.answer(t(admin_lang, "admin_no_rights"))
        return

    args = (message.text or "").split(maxsplit=1)
    if len(args) < 2:
        await message.answer(t(admin_lang, "broadcast_usage"), parse_mode="HTML")
        return

    raw_text = args[1]
    if "|||" in raw_text:
        ru_text, en_text = [part.strip() for part in raw_text.split("|||", 1)]
    else:
        ru_text = en_text = raw_text

    user_ids = await get_all_user_ids()
    await message.answer(t(admin_lang, "broadcast_start", count=len(user_ids)))

    success_count = 0
    fail_count = 0

    for user_id in user_ids:
        try:
            user_lang = await get_user_language(user_id)
            text = en_text if user_lang == "en" else ru_text
            user_group = await get_user_group(user_id)
            if user_group:  # отправляем клавиатуру только тем, у кого уже выбрана группа
                await message.bot.send_message(user_id, text, parse_mode="HTML", reply_markup=main_menu_kb(user_lang))
            else:
                await message.bot.send_message(user_id, text, parse_mode="HTML")
            success_count += 1
        except Exception as e:
            logger.warning(f"Не удалось отправить сообщение пользователю {user_id}: {e}")
            fail_count += 1
        await asyncio.sleep(0.05)  # пауза, чтобы Telegram не ограничил скорость

    await message.answer(t(admin_lang, "broadcast_done", ok=success_count, fail=fail_count))


# ============================================================
#  КНОПКИ ВЫБОРА ЯЗЫКА И ДЕЙСТВИЯ (callback)
# ============================================================

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
    await callback.message.answer(t(lang, "groups_message"), parse_mode="HTML")


@router.callback_query(F.data == "action_language")
async def action_change_language(callback: CallbackQuery, state: FSMContext):
    lang = await get_user_language(callback.from_user.id)
    await state.set_state(Register.waiting_language)
    await callback.answer()
    await callback.message.answer(
        t(lang, "choose_lang"),
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
        await callback.message.answer(t(lang, "enter_group"), parse_mode="HTML")
        return

    await state.clear()
    await callback.answer()
    await callback.message.answer(
        t(lang, "welcome_back", group=esc(group)),
        reply_markup=main_menu_kb(lang),
        parse_mode="HTML"
    )


# ============================================================
#  КНОПКИ ГЛАВНОГО МЕНЮ
# ============================================================

@router.message(F.text.in_([t("ru", "today"), t("en", "today")]))
async def show_today(message: Message):
    lang = await get_user_language(message.from_user.id)
    await show_day(message, today_date(), lang)


@router.message(F.text.in_([t("ru", "tomorrow"), t("en", "tomorrow")]))
async def show_tomorrow(message: Message):
    lang = await get_user_language(message.from_user.id)
    await show_day(message, today_date() + timedelta(days=1), lang)


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


@router.message(F.text.in_([
    t("ru", "next_week"), t("en", "next_week"),
    t("ru", "next_week_btn"), t("en", "next_week_btn"),
]))
async def show_next_week(message: Message):
    lang = await get_user_language(message.from_user.id)

    # Понедельник следующей недели
    today = today_date()
    next_monday = today + timedelta(days=7 - today.weekday())

    schedule = await get_schedule_for_user(message.from_user.id, next_monday)
    if schedule is None:
        await message.answer(t(lang, "error_schedule"), parse_mode="HTML")
        return

    days = get_week_dates(next_monday)
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


@router.message(F.text.in_([t("ru", "settings_btn"), t("en", "settings_btn")]))
async def settings(message: Message, state: FSMContext):
    lang = await get_user_language(message.from_user.id)
    group = await get_user_group(message.from_user.id)
    await message.answer(
        t(lang, "settings", group=esc(group) if group else "—"),
        parse_mode="HTML"
    )
    await state.set_state(Register.waiting_group)


@router.message(F.text.in_([t("ru", "language_btn"), t("en", "language_btn")]))
async def change_language(message: Message, state: FSMContext):
    lang = await get_user_language(message.from_user.id)
    await state.set_state(Register.waiting_language)
    await message.answer(
        t(lang, "choose_lang"),
        reply_markup=language_kb(),
        parse_mode="HTML"
    )


@router.message(F.text.in_([t("ru", "groups_btn"), t("en", "groups_btn")]))
async def show_groups(message: Message):
    await cmd_groups(message)


@router.message(F.text.in_([t("ru", "help_btn"), t("en", "help_btn")]))
async def show_help(message: Message):
    await cmd_help(message)


# ============================================================
#  ОБРАБОТЧИКИ СОСТОЯНИЙ (ввод группы и даты)
#  Они стоят ПОСЛЕ кнопок меню: иначе, пока бот ждёт дату,
#  нажатие «Настройки» было бы принято за неверную дату.
# ============================================================

@router.message(Register.waiting_custom_date)
async def process_custom_date(message: Message, state: FSMContext):
    lang = await get_user_language(message.from_user.id)
    day = parse_user_date(message.text)
    if day is None:
        await message.answer(t(lang, "date_invalid"), parse_mode="HTML")
        return

    await state.clear()
    await show_day(message, day, lang)


@router.message(Register.waiting_group)
async def process_group(message: Message, state: FSMContext):
    lang = await get_user_language(message.from_user.id)
    group = (message.text or "").strip()

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
        t(lang, "group_saved", group=esc(group)),
        reply_markup=main_menu_kb(lang),
        parse_mode="HTML"
    )


@router.message(F.text.in_([t("ru", "donate_btn"), t("en", "donate_btn")]))
async def show_donate(message: Message):
    lang = await get_user_language(message.from_user.id)
    
    # Создаём инлайн-кнопку с реальной ссылкой на донат
    # ЗАМЕНИ 'https://boosty.to/ТВОЙ_НИК' на свою реальную ссылку (Boosty, ЮMoney, Telegram Donate и т.д.)
    donate_link = "https://messenger.sbrf.ru/sl/XdhKV49gaUoU7hhyy" 
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💖 Поддержать разработчицу", url=donate_link)]
    ])
    
    await message.answer(
        t(lang, "donate_message"), 
        reply_markup=kb, 
        parse_mode="HTML"
    )

# ============================================================
#  ЗАПАСНЫЕ ОБРАБОТЧИКИ — ВСЕГДА В САМОМ КОНЦЕ ФАЙЛА!
# ============================================================

@router.callback_query()
async def fallback_callback(call: CallbackQuery, state: FSMContext):
    logger.warning("Необработанная кнопка: data=%r, state=%r",
                   call.data, await state.get_state())
    lang = await get_user_language(call.from_user.id)
    await call.answer(t(lang, "fallback_callback"), show_alert=True)


@router.message()
async def fallback_message(message: Message, state: FSMContext):
    logger.warning("Необработанное сообщение: text=%r, state=%r",
                   message.text, await state.get_state())
    lang = await get_user_language(message.from_user.id)
    await message.answer(t(lang, "fallback_message"))
