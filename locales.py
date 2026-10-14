TEXTS = {
    "ru": {
        "welcome": (
            "👋 Привет! Я — бот расписания БФУ им. И. Канта.\n\n"
            "🎓 Я помогу тебе всегда быть в курсе:\n"
            "• 📅 какие пары сегодня и завтра\n"
            "• 🗓 расписание на всю неделю\n"
            "• 📆 пары на любую дату\n\n"
            "🌟 Давай начнём! Сначала выбери язык:"
        ),
        "enter_group": (
            "📚 Отлично! Теперь введи номер своей академической группы.\n\n"
            "💡 <b>Формат:</b> <code>уровень_направление_год_номер</code>\n"
            "📌 <b>Пример:</b> <code>03_ФИИТ_26_02</code>\n\n"
            "🔍 <b>Расшифровка:</b>\n"
            "• <b>03</b> — уровень образования (бакалавриат)\n"
            "• <b>ФИИТ</b> — направление подготовки\n"
            "• <b>26</b> — год поступления (2026)\n"
            "• <b>02</b> — номер группы\n\n"
            "👇 Введи свою группу:"
        ),
        "group_saved": "✅ Группа <b>{group}</b> сохранена! Теперь выбери, что показать:",
        "group_invalid": "❌ Группа указана неверно. Проверь формат и попробуй ещё раз:",
        "fetch_error": "❌ Не удалось получить расписание для этой группы. Проверь номер:",
        "choose_lang": "🌍 Выбери язык / Choose language:",
        "lang_set": "✅ Язык установлен: Русский",
        "no_classes": "Пар нет — можно отдыхать! 🎉",
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
        "welcome_back": "👋 С возвращением!\n\n🎓 Твоя группа: <b>{group}</b>\n\n👇 Выбери, что посмотреть:",
    },
    "en": {
        "welcome": (
            "👋 Hello! I'm the BFU Im. Kant schedule bot.\n\n"
            "🎓 I'll help you stay on top of your classes:\n"
            "• 📅 today's and tomorrow's schedule\n"
            "• 🗓 full week view\n"
            "• 📆 any specific date\n\n"
            "🌟 Let's start! First, choose your language:"
        ),
        "enter_group": (
            "📚 Great! Now enter your academic group number.\n\n"
            "💡 <b>Format:</b> <code>level_program_year_number</code>\n"
            "📌 <b>Example:</b> <code>03_ФИИТ_26_02</code>\n\n"
            "🔍 <b>Breakdown:</b>\n"
            "• <b>03</b> — education level (bachelor's)\n"
            "• <b>ФИИТ</b> — program of study\n"
            "• <b>26</b> — enrollment year (2026)\n"
            "• <b>02</b> — group number\n\n"
            "👇 Enter your group:"
        ),
        "group_saved": "✅ Group <b>{group}</b> saved! Now choose what to show:",
        "group_invalid": "❌ Invalid group number. Check the format and try again:",
        "fetch_error": "❌ Could not fetch schedule for this group. Check the number:",
        "choose_lang": "🌍 Choose language / Выбери язык:",
        "lang_set": "✅ Language set: English",
        "no_classes": "No classes today — enjoy your free time! 🎉",
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
        "welcome_back": "👋 Welcome back!\n\n🎓 Your group: <b>{group}</b>\n\n👇 Choose what to view:",
    }
}


def t(lang: str, key: str, **kwargs) -> str:
    text = TEXTS.get(lang, TEXTS["ru"]).get(key, key)
    return text.format(**kwargs) if kwargs else text
