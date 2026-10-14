TEXTS = {
    "ru": {
        "welcome": "Привет! 👋 Я бот расписания БФУ им. И. Канта.",
        "enter_group": "Введи номер своей академической группы (например, <code>123456</code>):",
        "group_saved": "✅ Группа <b>{group}</b> сохранена!",
        "group_invalid": "❌ Группа указана неверно. Попробуй ещё раз:",
        "fetch_error": "❌ Не удалось получить расписание для этой группы. Проверь номер:",
        "choose_lang": "🌍 Выбери язык / Choose language:",
        "lang_set": "✅ Язык установлен: Русский",
        "no_classes": "Пар нет, можно отдыхать! 🎉",
        "error_schedule": "❌ Ошибка получения расписания. Попробуй позже.",
        "settings": "Текущая группа: <b>{group}</b>\n\nВведи новый номер группы:",
        "today": "📅 Сегодня",
        "tomorrow": "📆 Завтра",
        "week": "🗓 На неделю",
        "custom_date": "📆 Выбрать дату",
        "settings_btn": "⚙️ Настройки",
        "language_btn": "🌍 Язык / Language",
        "enter_date": "Введи дату в формате <code>ДД.ММ.ГГГГ</code> (например, <code>15.10.2026</code>):",
        "date_invalid": "❌ Неверный формат даты. Попробуй ещё раз:",
        "welcome_back": "С возвращением! 👋\nТвоя группа: <b>{group}</b>",
    },
    "en": {
        "welcome": "Hello! 👋 I'm the BFU Im. Kant schedule bot.",
        "enter_group": "Enter your academic group number (e.g., <code>123456</code>):",
        "group_saved": "✅ Group <b>{group}</b> saved!",
        "group_invalid": "❌ Invalid group number. Try again:",
        "fetch_error": "❌ Could not fetch schedule for this group. Check the number:",
        "choose_lang": "🌍 Choose language / Выбери язык:",
        "lang_set": "✅ Language set: English",
        "no_classes": "No classes today, enjoy your free time! 🎉",
        "error_schedule": "❌ Error fetching schedule. Try again later.",
        "settings": "Current group: <b>{group}</b>\n\nEnter new group number:",
        "today": "📅 Today",
        "tomorrow": "📆 Tomorrow",
        "week": "🗓 Week",
        "custom_date": "📆 Custom date",
        "settings_btn": "⚙️ Settings",
        "language_btn": "🌍 Language / Язык",
        "enter_date": "Enter date in format <code>DD.MM.YYYY</code> (e.g., <code>15.10.2026</code>):",
        "date_invalid": "❌ Invalid date format. Try again:",
        "welcome_back": "Welcome back! 👋\nYour group: <b>{group}</b>",
    }
}


def t(lang: str, key: str, **kwargs) -> str:
    text = TEXTS.get(lang, TEXTS["ru"]).get(key, key)
    return text.format(**kwargs) if kwargs else text