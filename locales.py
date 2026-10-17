# locales.py

import logging

logger = logging.getLogger(__name__)

# Эти два текста одинаковы для обоих языков: в них сразу и русский, и английский,
# потому что пользователь ещё не выбрал язык.
WELCOME_BILINGUAL = (
    "👋 <b>Привет! / Hello!</b>\n\n"
    "🎓 <b>Я — бот расписания БФУ им. И. Канта.</b>\n"
    "🎓 <b>I am the BFU Im. Kant schedule bot.</b>\n\n"
    "📋 <b>Как пользоваться / How to use:</b>\n"
    " 1️⃣ Выбери язык / Choose language\n"
    " 2️⃣ Введи номер группы / Enter group number\n"
    " 3️⃣ Смотри расписание / Check schedule\n\n"
    "⚙️ <b>Кнопки меню / Menu buttons:</b>\n"
    " 📅 <b>Сегодня / Today</b> — пары на сегодня / today's classes\n"
    " 📆 <b>Завтра / Tomorrow</b> — пары на завтра / tomorrow's classes\n"
    " 🗓 <b>На неделю / Week</b> — расписание на неделю / schedule for the week\n"
    " ➡️ <b>Следующая неделя / Next week</b> — расписание на следующую неделю / schedule for next week\n"
    " 📆 <b>Дата / Date</b> — любая дата: прошлая или будущая / any date, past or future\n"
    " ⚙️ <b>Настройки / Settings</b> — сменить группу / change group\n"
    " 🌍 <b>Язык / Language</b> — сменить язык / change language\n"
    " 📋 <b>Группы / Groups</b> — список специальностей / list of programs\n"
    " ❓ <b>Помощь / Help</b> — подробный гайд / detailed guide\n\n"
    " 💖 <b>Поддержать / Support</b> — поддержать разработчицу / support the developer\n\n"
    " 🆘 <b>Нужна помощь? / Need help?</b>\n"
    "Если вашей группы нет или бот работает некорректно, напишите в нашу супер-поддержку / "
    "If your group is missing or the bot misbehaves, contact our super-support: @alexa_ash_avery\n\n"
    "👇 <b>Выберите язык / Choose language:</b>"
)

RESET_SUCCESS = "🔄 <b>Данные сброшены! / Data reset!</b>\n\n👇 <b>Выберите язык / Choose language:</b>"

CHOOSE_LANG = "🌍 <b>Выбери язык / Choose language:</b>"


TEXTS = {
    "ru": {
        "welcome_bilingual": WELCOME_BILINGUAL,
        "after_language": (
            "✅ <b>Отлично!</b>\n\n"
            "👇 <b>Выбери дальнейшее действие:</b>"
        ),
        "choose_lang": "🌍 <b>Выбери язык:</b>",
        "next_week": "🗓 На следующую неделю",
        "next_week_btn": "➡️ Следующая неделя",
        "group_saved": "✅ <b>Группа {group} сохранена!</b>\n\n🎯 Теперь выбери, что показать:",
        "enter_group": "👇 <b>Введи номер группы:</b>\n\n💡 Например: <code>03_ФИИТ_26_2</code>",
        "group_invalid": (
            "❌ <b>Группа указана неверно.</b>\n\n"
            "💡 Проверь формат: <code>03_ФИИТ_26_2</code>\n"
            "👇 <b>Попробуй ещё раз:</b>"
        ),
        "group_not_found": (
            "❌ <b>Группа не найдена в базе БФУ.</b>\n\n"
            "💡 Возможно, ты ошибся в названии.\n"
            "🆘 Если группы нет в списке, напиши: @alexa_ash_avery\n\n"
            "👇 <b>Попробуй ввести группу ещё раз:</b>"
        ),
        "fetch_error": (
            "❌ <b>Не удалось получить расписание.</b>\n\n"
            "💡 Возможно, сайт БФУ временно недоступен.\n"
            "🆘 Если проблема не решается, напиши: @alexa_ash_avery"
        ),
        "choose_lang": CHOOSE_LANG,
        "lang_set": "✅ <b>Язык установлен: Русский</b>",
        "no_classes": "🎉 <b>Пар нет — можно отдыхать!</b>",
        "error_schedule": (
            "❌ <b>Ошибка получения расписания.</b>\n\n"
            "🆘 Если проблема сохраняется, напиши: @alexa_ash_avery"
        ),
        "settings": (
            "⚙️ <b>Настройки</b>\n\n"
            "📚 <b>Текущая группа:</b> {group}\n\n"
            "👇 <b>Введи новый номер группы:</b>"
        ),
        "today": "📅 Сегодня",
        "tomorrow": "📆 Завтра",
        "week": "🗓 На неделю",
        "custom_date": "📆 Дата",
        "settings_btn": "⚙️ Настройки",
        "language_btn": "🌍 Язык",
        "groups_btn": "📋 Группы",
        "help_btn": "❓ Помощь",
        "changelog_btn": "🆕 Что нового?",
        "menu_btn": "🏠 Меню",
        "enter_date": (
            "📅 <b>Введи любую дату — из прошлого или из будущего.</b>\n\n"
            "📌 <b>Форматы:</b>\n"
            " • <code>ДД.ММ.ГГГГ</code> — например, <code>15.10.2026</code>\n"
            " • <code>ДД.ММ</code> — текущий год, например, <code>15.10</code>"
        ),
        "date_invalid": (
            "❌ <b>Не получилось разобрать дату.</b>\n\n"
            "💡 Правильные форматы: <code>ДД.ММ.ГГГГ</code> или <code>ДД.ММ</code>\n"
            "📆 Год — от 2000 до 2100.\n"
            "👇 <b>Попробуй ещё раз:</b>"
        ),
        "welcome_back": (
            "👋 <b>С возвращением!</b>\n\n"
            "🎓 <b>Твоя группа:</b> {group}\n\n"
            "🎯 <b>Выбери действие:</b>"
        ),
        "reset_success": RESET_SUCCESS,
        "help_message": (
            "❓ <b>Помощь</b>\n\n"
            "📚 <b>Основные команды:</b>\n"
            " • <code>/start</code> — начать работу с ботом\n"
            " • <code>/reset</code> — сбросить настройки\n"
            " • <code>/groups</code> — список всех групп БФУ\n"
            " • <code>/changelog</code> — что нового в боте\n"
            " • <code>/help</code> — показать это сообщение\n\n"
            "📆 <b>Кнопка «Дата»</b> показывает расписание на любой день — "
            "и из прошлого, и из будущего.\n\n"
            "🆘 <b>Нужна помощь?</b>\n"
            "Напишите супер-поддержке: @alexa_ash_avery"
        ),
        "groups_message": (
            "📋 <b>Список всех групп БФУ</b>\n\n"
            "🔗 <b>Посмотри на сайте:</b> https://schedule.kantiana.ru/\n\n"
            "💡 <b>Как найти свою группу:</b>\n"
            " 1️⃣ Открой сайт\n"
            " 2️⃣ Выбери свой институт/колледж\n"
            " 3️⃣ Найди направление и курс\n"
            " 4️⃣ Скопируй название группы (например, <code>03_ФИИТ_26_2</code>)\n"
            " 5️⃣ Введи его сюда\n\n"
            "🆘 <b>Не можешь найти?</b>\n"
            "Напиши супер-поддержке: @alexa_ash_avery"
        ),
        # --- служебные сообщения ---
        "changelog_header": "📋 <b>История изменений:</b>",
        "fallback_message": "Не понял 🤔 Нажми /start, чтобы вернуться в меню",
        "fallback_callback": "Кнопка устарела, нажми /start",
        "admin_no_rights": "⛔ У вас нет прав для этой команды.",
        "broadcast_usage": (
            "📢 <b>Использование:</b>\n"
            "<code>/broadcast Текст сообщения</code>\n\n"
            "Чтобы каждый получил текст на своём языке, раздели русскую и английскую "
            "части тремя символами «|»:\n"
            "<code>/broadcast Привет! ||| Hello!</code>"
        ),
        "broadcast_start": "📤 Начинаю рассылку {count} пользователям...",
        "broadcast_done": "✅ Рассылка завершена!\n📤 Успешно: {ok}\n❌ Ошибок: {fail}",

        "donate_btn": "💖 Поддержать разработчицу",
        "donate_message": (
            "☕ <b>Разработчице заплатите чеканной монетой на кофеёк!</b>\n\n"
            "Ваша поддержка помогает делать бота быстрее, стабильнее и еще круче.\n\n"
            "💳 <b>Как поддержать:</b>\n"
            "   • Сбор на Сбере: https://messenger.sbrf.ru/sl/XdhKV49gaUoU7hhyy\n\n"
            "Спасибо, что вы с нами! ❤️"
        ),
    },
    "en": {
        "welcome_bilingual": WELCOME_BILINGUAL,
        "after_language": (
            "✅ <b>Great!</b>\n\n"
            "👇 <b>Choose your next action:</b>"
        ),
        "choose_lang": "🌍 <b>Choose a language:</b>",
        "next_week": "🗓 For next week",
        "next_week_btn": "➡️ Next week",
        "group_saved": "✅ <b>Group {group} saved!</b>\n\n🎯 Now choose what to show:",
        "enter_group": "👇 <b>Enter your group number:</b>\n\n💡 For example: <code>03_ФИИТ_26_2</code>",
        "group_invalid": (
            "❌ <b>Invalid group number.</b>\n\n"
            "💡 Check the format: <code>03_ФИИТ_26_02</code>\n"
            "👇 <b>Try again:</b>"
        ),
        "group_not_found": (
            "❌ <b>Group not found in BFU database.</b>\n\n"
            "💡 Maybe there is a typo in the name.\n"
            "🆘 If your group is missing, contact: @alexa_ash_avery\n\n"
            "👇 <b>Try entering the group again:</b>"
        ),
        "fetch_error": (
            "❌ <b>Could not fetch schedule.</b>\n\n"
            "💡 The BFU website may be temporarily unavailable.\n"
            "🆘 If the problem persists, contact: @alexa_ash_avery"
        ),
        "choose_lang": CHOOSE_LANG,
        "lang_set": "✅ <b>Language set: English</b>",
        "no_classes": "🎉 <b>No classes — enjoy your free time!</b>",
        "error_schedule": (
            "❌ <b>Error fetching schedule.</b>\n\n"
            "🆘 If the problem persists, contact: @alexa_ash_avery"
        ),
        "settings": (
            "⚙️ <b>Settings</b>\n\n"
            "📚 <b>Current group:</b> {group}\n\n"
            "👇 <b>Enter new group number:</b>"
        ),
        "today": "📅 Today",
        "tomorrow": "📆 Tomorrow",
        "week": "🗓 Week",
        "custom_date": "📆 Date",
        "settings_btn": "⚙️ Settings",
        "language_btn": "🌍 Language",
        "groups_btn": "📋 Groups",
        "help_btn": "❓ Help",
        "changelog_btn": "🆕 What's new?",
        "menu_btn": "🏠 Menu",
        "enter_date": (
            "📅 <b>Enter any date — past or future.</b>\n\n"
            "📌 <b>Formats:</b>\n"
            " • <code>DD.MM.YYYY</code> — e.g. <code>15.10.2026</code>\n"
            " • <code>DD.MM</code> — current year, e.g. <code>15.10</code>"
        ),
        "date_invalid": (
            "❌ <b>Could not read the date.</b>\n\n"
            "💡 Correct formats: <code>DD.MM.YYYY</code> or <code>DD.MM</code>\n"
            "📆 The year must be between 2000 and 2100.\n"
            "👇 <b>Try again:</b>"
        ),
        "welcome_back": (
            "👋 <b>Welcome back!</b>\n\n"
            "🎓 <b>Your group:</b> {group}\n\n"
            "🎯 <b>Choose an action:</b>"
        ),
        "reset_success": RESET_SUCCESS,
        "help_message": (
            "❓ <b>Help</b>\n\n"
            "📚 <b>Main commands:</b>\n"
            " • <code>/start</code> — start working with the bot\n"
            " • <code>/reset</code> — reset settings\n"
            " • <code>/groups</code> — show all BFU groups\n"
            " • <code>/changelog</code> — what's new in the bot\n"
            " • <code>/help</code> — show this message\n\n"
            "📆 <b>The “Date” button</b> shows the schedule for any day — "
            "past or future.\n\n"
            "🆘 <b>Need help?</b>\n"
            "Contact our super-support: @alexa_ash_avery"
        ),
        "groups_message": (
            "📋 <b>List of all BFU groups</b>\n\n"
            "🔗 <b>Check the website:</b> https://schedule.kantiana.ru/\n\n"
            "💡 <b>How to find your group:</b>\n"
            " 1️⃣ Open the website\n"
            " 2️⃣ Choose your institute/college\n"
            " 3️⃣ Find your program and year\n"
            " 4️⃣ Copy the group name (e.g., <code>03_ФИИТ_26_2</code>)\n"
            " 5️⃣ Enter it here\n\n"
            "🆘 <b>Can't find it?</b>\n"
            "Contact our super-support: @alexa_ash_avery"
        ),
        # --- service messages ---
        "changelog_header": "📋 <b>Changelog:</b>",
        "fallback_message": "I didn't get that 🤔 Press /start to go back to the menu",
        "fallback_callback": "This button is outdated, press /start",
        "admin_no_rights": "⛔ You don't have permission for this command.",
        "broadcast_usage": (
            "📢 <b>Usage:</b>\n"
            "<code>/broadcast Message text</code>\n\n"
            "To send each user the text in their own language, separate the Russian "
            "and English parts with three “|” symbols:\n"
            "<code>/broadcast Привет! ||| Hello!</code>"
        ),
        "broadcast_start": "📤 Starting broadcast to {count} users...",
        "broadcast_done": "✅ Broadcast finished!\n📤 Sent: {ok}\n❌ Failed: {fail}",

        "donate_btn": "💖 Support the developer",
        "donate_message": (
            "☕ <b>Toss a coin to your developer for a coffee!</b>\n\n"
            "Your support helps make the bot faster, more stable, and even better.\n\n"
            "💳 <b>How to support:</b>\n"
            "   • Sberbank collection link: https://messenger.sbrf.ru/sl/XdhKV49gaUoU7hhyy\n\n"
            "Thanks for being with us! ❤️"
),
    },
}

# Названия дней недели (понедельник = индекс 0, как в Python)
WEEKDAYS = {
    "ru": ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"],
    "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
}

# Самопроверка: в обоих языках должны быть одни и те же ключи.
_missing = set(TEXTS["ru"]) ^ set(TEXTS["en"])
if _missing:
    logger.warning("⚠️ Ключи есть не в обоих языках: %s", sorted(_missing))


def t(lang: str, key: str, **kwargs) -> str:
    """Берёт текст по языку и ключу. Если ключа нет в выбранном языке,
    берёт русский; если нет и там, возвращает сам ключ."""
    text = TEXTS.get(lang, TEXTS["ru"]).get(key, TEXTS["ru"].get(key, key))
    if not kwargs:
        return text
    try:
        return text.format(**kwargs)
    except (KeyError, IndexError) as e:
        logger.error("Ошибка форматирования текста key=%r lang=%r: %r", key, lang, e)
        return text
