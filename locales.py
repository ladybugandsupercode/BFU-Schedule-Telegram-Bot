TEXTS = {
    "ru": {
        "welcome_bilingual": (
            "👋 <b>Привет! / Hello!</b>\n\n"
            "🎓 <b>Я — бот расписания БФУ им. И. Канта.</b>\n"
            "🎓 <b>I am the BFU Im. Kant schedule bot.</b>\n\n"
            "📋 <b>Как пользоваться / How to use:</b>\n"
            "1️⃣ Выбери язык / Choose language\n"
            "2️⃣ Введи номер группы / Enter group number\n"
            "3️⃣ Смотри расписание / Check schedule\n\n"
            "⚙️ <b>Кнопки меню / Menu buttons:</b>\n"
            "📅 <b>Сегодня / Today</b> — пары на сегодня\n"
            "📆 <b>Завтра / Tomorrow</b> — пары на завтра\n"
            "🗓 <b>На неделю / Week</b> — расписание на 7 дней\n"
            "📆 <b>Дата / Date</b> — расписание на конкретный день\n"
            "⚙️ <b>Настройки / Settings</b> — сменить группу\n"
            "🌍 <b>Язык / Language</b> — сменить язык\n"
            "📋 <b>Группы / Groups</b> — список всех специальностей\n"
            "❓ <b>Помощь / Help</b> — подробный гайд\n\n"
            "🆘 <b>Нужна помощь? / Need help?</b>\n"
            "Если вашей группы нет или бот работает некорректно, напишите: @alexa_ash_avery\n\n"
            "👇 <b>Выберите язык / Choose language:</b>"
        ),
        "after_language": (
            "✅ <b>Отлично! / Great!</b>\n\n"
            "👇 <b>Выберите действие / Choose an action:</b>"
        ),
        "enter_group": (
            "📚 <b>Введи номер своей академической группы.</b>\n\n"
            "💡 <b>Формат:</b> <code>уровень_направление_год_номер</code>\n"
            "📌 <b>Пример:</b> <code>03_ФИИТ_26_02</code>\n\n"
            "🔍 <b>Расшифровка:</b>\n"
            "• <b>03</b> — уровень образования (бакалавриат)\n"
            "• <b>ФИИТ</b> — направление подготовки\n"
            "• <b>26</b> — год поступления (2026)\n"
            "• <b>02</b> — номер группы\n\n"
            "📋 <b>Не знаешь свою группу?</b>\n"
            "Нажми кнопку <b>📋 Группы</b> или напиши /groups\n\n"
            "👇 <b>Введи свою группу:</b>"
        ),
        "group_saved": "✅ <b>Группа {group} сохранена!</b>\n\n🎯 Теперь выбери, что показать:",
        "group_invalid": (
            "❌ <b>Группа указана неверно.</b>\n\n"
            "💡 Проверь формат: <code>03_ФИИТ_26_02</code>\n"
            "👇 <b>Попробуй ещё раз:</b>"
        ),
        "group_not_found": (
            "❌ <b>Группа не найдена в базе БФУ.</b>\n\n"
            "💡 Возможно, ты ошиблась в названии.\n"
            "🆘 Если группы нет в списке, напиши: @alexa_ash_avery\n\n"
            "👇 <b>Попробуй ввести группу ещё раз:</b>"
        ),
        "fetch_error": (
            "❌ <b>Не удалось получить расписание.</b>\n\n"
            "💡 Возможно, сайт БФУ временно недоступен.\n"
            "🆘 Если проблема не решается, напиши: @alexa_ash_avery"
        ),
        "choose_lang": "🌍 <b>Выбери язык / Choose language:</b>",
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
        "enter_date": "📅 <b>Введи дату в формате <code>ДД.ММ.ГГГГ</code></b>\n\n📌 <b>Пример:</b> <code>15.10.2026</code>",
        "date_invalid": "❌ <b>Неверный формат даты.</b>\n\n💡 Правильный формат: <code>ДД.ММ.ГГГГ</code>",
        "welcome_back": (
            "👋 <b>С возвращением!</b>\n\n"
            "🎓 <b>Твоя группа:</b> {group}\n\n"
            "🎯 <b>Выбери действие:</b>"
        ),
        "reset_success": "🔄 <b>Данные сброшены!</b>\n\n👇 <b>Выберите язык для продолжения:</b>",
        "help_message": (
            "❓ <b>Помощь / Help</b>\n\n"
            "📚 <b>Основные команды:</b>\n"
            "• <code>/start</code> — начать работу с ботом\n"
            "• <code>/reset</code> — сбросить настройки\n"
            "• <code>/groups</code> — список всех групп БФУ\n"
            "• <code>/help</code> — показать это сообщение\n\n"
            "🆘 <b>Нужна помощь?</b>\n"
            "Напишите: @alexa_ash_avery"
        ),
    },
    "en": {
        "after_language": "✅ <b>Great!</b>\n\n👇 <b>Choose an action:</b>",
        "enter_group": (
            "📚 <b>Enter your academic group number.</b>\n\n"
            "💡 <b>Format:</b> <code>level_program_year_number</code>\n"
            "📌 <b>Example:</b> <code>03_ФИИТ_26_02</code>\n\n"
            "🔍 <b>Breakdown:</b>\n"
            "• <b>03</b> — education level (bachelor's)\n"
            "• <b>ФИИТ</b> — program of study\n"
            "• <b>26</b> — enrollment year (2026)\n"
            "• <b>02</b> — group number\n\n"
            "📋 <b>Don't know your group?</b>\n"
            "Press <b>📋 Groups</b> button or type /groups\n\n"
            "👇 <b>Enter your group:</b>"
        ),
        "group_saved": "✅ <b>Group {group} saved!</b>\n\n🎯 Now choose what to show:",
        "group_invalid": "❌ <b>Invalid group number.</b>\n\n💡 Check the format: <code>03_ФИИТ_26_02</code>\n👇 <b>Try again:</b>",
        "group_not_found": "❌ <b>Group not found in BFU database.</b>\n\n🆘 If your group is missing, contact: @alexa_ash_avery\n\n👇 <b>Try entering the group again:</b>",
        "fetch_error": "❌ <b>Could not fetch schedule.</b>\n\n🆘 If the problem persists, contact: @alexa_ash_avery",
        "choose_lang": "🌍 <b>Choose language / Выбери язык:</b>",
        "lang_set": "✅ <b>Language set: English</b>",
        "no_classes": "🎉 <b>No classes today — enjoy your free time!</b>",
        "error_schedule": "❌ <b>Error fetching schedule.</b>\n\n🆘 If the problem persists, contact: @alexa_ash_avery",
        "settings": "⚙️ <b>Settings</b>\n\n📚 <b>Current group:</b> {group}\n\n👇 <b>Enter new group number:</b>",
        "today": "📅 Today",
        "tomorrow": "📆 Tomorrow",
        "week": "🗓 Week",
        "custom_date": "📆 Date",
        "settings_btn": "⚙️ Settings",
        "language_btn": "🌍 Language",
        "groups_btn": "📋 Groups",
        "help_btn": "❓ Help",
        "enter_date": "📅 <b>Enter date in format <code>DD.MM.YYYY</code></b>\n\n📌 <b>Example:</b> <code>15.10.2026</code>",
        "date_invalid": "❌ <b>Invalid date format.</b>\n\n💡 Correct format: <code>DD.MM.YYYY</code>",
        "welcome_back": "👋 <b>Welcome back!</b>\n\n🎓 <b>Your group:</b> {group}\n\n🎯 <b>Choose an action:</b>",
        "reset_success": "🔄 <b>Data reset!</b>\n\n👇 <b>Choose language to continue:</b>",
        "help_message": (
            "❓ <b>Help</b>\n\n"
            "📚 <b>Main commands:</b>\n"
            "• <code>/start</code> — start working with the bot\n"
            "• <code>/reset</code> — reset settings\n"
            "• <code>/groups</code> — show all BFU groups\n"
            "• <code>/help</code> — show this message\n\n"
            "🆘 <b>Need help?</b>\n"
            "Contact: @alexa_ash_avery"
        ),
    }
}

def t(lang: str, key: str, **kwargs) -> str:
    text = TEXTS.get(lang, TEXTS["ru"]).get(key, TEXTS["ru"].get(key, key))
    return text.format(**kwargs) if kwargs else text
