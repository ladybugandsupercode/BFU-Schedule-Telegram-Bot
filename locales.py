TEXTS = {
    "ru": {
        "welcome_bilingual": (
            "👋 **Привет! / Hello!**\n\n"
            "🎓 **Я — бот расписания БФУ им. И. Канта.**\n"
            "🎓 **I am the BFU Im. Kant schedule bot.**\n\n"
            "📋 **Как пользоваться / How to use:**\n"
            "1️⃣ Выбери язык / Choose language\n"
            "2️⃣ Введи номер группы / Enter group number\n"
            "3️⃣ Смотри расписание / Check schedule\n\n"
            "⚙️ **Кнопки меню / Menu buttons:**\n"
            "📅 **Сегодня / Today** — пары на сегодня\n"
            "📆 **Завтра / Tomorrow** — пары на завтра\n"
            "🗓 **На неделю / Week** — расписание на 7 дней\n"
            "📆 **Дата / Date** — расписание на конкретный день\n"
            "⚙️ **Настройки / Settings** — сменить группу\n"
            "🌍 **Язык / Language** — сменить язык\n"
            "📋 **Группы / Groups** — список всех специальностей\n"
            "❓ **Помощь / Help** — подробный гайд\n\n"
            "🆘 **Нужна помощь? / Need help?**\n"
            "Если вашей группы нет или бот работает некорректно, напишите: @alexa_ash_avery\n"
            "If your group is missing or the bot malfunctions, contact: @alexa_ash_avery\n\n"
            "👇 **Выберите язык / Choose language:**"
        ),
        "after_language": (
            "✅ **Отлично! / Great!**\n\n"
            "🎯 **Что дальше? / What's next?**\n\n"
            "📝 **Выбери действие / Choose an action:**"
        ),
        "enter_group": (
            "📚 **Введи номер своей академической группы.**\n\n"
            "💡 **Формат:** `уровень_направление_год_номер`\n"
            "📌 **Пример:** `03_ФИИТ_26_02`\n\n"
            "🔍 **Расшифровка:**\n"
            "• **03** — уровень образования (бакалавриат)\n"
            "• **ФИИТ** — направление подготовки\n"
            "• **26** — год поступления (2026)\n"
            "• **02** — номер группы\n\n"
            "📋 **Не знаешь свою группу?**\n"
            "Нажми кнопку '📋 Группы' или напиши /groups\n\n"
            "⚠️ **Важно:** Вводи группу!\n\n"
            "👇 **Введи свою группу:**"
        ),
        "group_saved": "✅ **Группа {group} сохранена!**\n\n🎯 Теперь выбери, что показать:",
        "group_invalid": (
            "❌ **Группа указана неверно.**\n\n"
            "💡 Проверь формат: `03_ФИИТ_26_02`\n"
            "📋 Или нажми кнопку '📋 Группы'\n\n"
            "👇 **Попробуй ещё раз:**"
        ),
        "group_not_found": (
            "❌ **Группа не найдена в базе БФУ.**\n\n"
            "💡 Возможно, ты ошибся в названии.\n"
            "📋 Нажми кнопку '📋 Группы' для проверки\n\n"
            "🆘 **Если вашей группы нет в списке:**\n"
            "Напишите: @alexa_ash_avery\n\n"
            "👇 **Попробуй ввести группу ещё раз:**"
        ),
        "fetch_error": (
            "❌ **Не удалось получить расписание.**\n\n"
            "💡 Возможно, группа указана неверно или сайт БФУ временно недоступен.\n\n"
            "🆘 **Если проблема не решается:**\n"
            "Напишите: @alexa_ash_avery"
        ),
        "choose_lang": "🌍 **Выбери язык / Choose language:**",
        "lang_set": "✅ **Язык установлен: Русский**",
        "no_classes": "🎉 **Пар нет — можно отдыхать!**",
        "error_schedule": (
            "❌ **Ошибка получения расписания.**\n\n"
            "💡 Попробуй позже или проверь группу\n\n"
            "🆘 **Если проблема сохраняется:**\n"
            "Напишите: @alexa_ash_avery"
        ),
        "settings": (
            "⚙️ **Настройки**\n\n"
            "📚 **Текущая группа:** {group}\n\n"
            "👇 **Введи новый номер группы:**"
        ),
        "today": "📅 Сегодня",
        "tomorrow": "📆 Завтра",
        "week": "🗓 На неделю",
        "custom_date": "📆 Дата",
        "settings_btn": "⚙️ Настройки",
        "language_btn": "🌍 Язык",
        "groups_btn": "📋 Группы",
        "help_btn": "❓ Помощь",
        "enter_date": "📅 **Введи дату в формате `ДД.ММ.ГГГГ`**\n\n📌 **Пример:** `15.10.2026`",
        "date_invalid": "❌ **Неверный формат даты.**\n\n💡 Правильный формат: `ДД.ММ.ГГГГ`\n📌 Пример: `15.10.2026`",
        "welcome_back": (
            "👋 **С возвращением!**\n\n"
            "🎓 **Твоя группа:** {group}\n\n"
            "🎯 **Выбери действие:**"
        ),
        "reset_success": "🔄 **Данные сброшены!**\n\n🎯 Давай начнём заново.\n\n🌍 **Выбери язык:**",
        "help_message": (
            "❓ **Помощь / Help**\n\n"
            "📚 **Основные команды:**\n"
            "• `/start` — начать работу с ботом\n"
            "• `/reset` — сбросить настройки и начать заново\n"
            "• `/groups` — показать список всех групп БФУ\n"
            "• `/help` — показать это сообщение\n\n"
            "🆘 **Нужна помощь?**\n"
            "Напишите: @alexa_ash_avery"
        ),
    },
    "en": {
        # Для английского мы используем те же ключи, но бот будет брать bilingual из 'ru' для первого экрана.
        # Остальные сообщения будут на английском, если пользователь его выбрал.
        "after_language": "✅ **Great!**\n\n🎯 **What's next?**\n\n📝 **Choose an action:**",
        "enter_group": (
            "📚 **Enter your academic group number.**\n\n"
            "💡 **Format:** `level_program_year_number`\n"
            "📌 **Example:** `03_ФИИТ_26_02`\n\n"
            "🔍 **Breakdown:**\n"
            "• **03** — education level (bachelor's)\n"
            "• **ФИИТ** — program of study\n"
            "• **26** — enrollment year (2026)\n"
            "• **02** — group number\n\n"
            "📋 **Don't know your group?**\n"
            "Press '📋 Groups' button or type /groups\n\n"
            "⚠️ **Important:** Enter the group!\n\n"
            "👇 **Enter your group:**"
        ),
        "group_saved": "✅ **Group {group} saved!**\n\n🎯 Now choose what to show:",
        "group_invalid": "❌ **Invalid group number.**\n\n💡 Check the format: `03_ФИИТ_26_02`\n👇 **Try again:**",
        "group_not_found": "❌ **Group not found in BFU database.**\n\n💡 You might have made a typo.\n🆘 **If your group is missing:**\nContact: @alexa_ash_avery\n\n👇 **Try entering the group again:**",
        "fetch_error": "❌ **Could not fetch schedule.**\n\n💡 The group might be incorrect or BFU website is temporarily unavailable.\n🆘 **If the problem persists:**\nContact: @alexa_ash_avery",
        "choose_lang": "🌍 **Choose language / Выбери язык:**",
        "lang_set": "✅ **Language set: English**",
        "no_classes": "🎉 **No classes today — enjoy your free time!**",
        "error_schedule": "❌ **Error fetching schedule.**\n\n💡 Try again later or verify the group.\n🆘 **If the problem persists:**\nContact: @alexa_ash_avery",
        "settings": "⚙️ **Settings**\n\n📚 **Current group:** {group}\n\n👇 **Enter new group number:**",
        "today": "📅 Today",
        "tomorrow": "📆 Tomorrow",
        "week": "🗓 Week",
        "custom_date": "📆 Date",
        "settings_btn": "⚙️ Settings",
        "language_btn": "🌍 Language",
        "groups_btn": "📋 Groups",
        "help_btn": "❓ Help",
        "enter_date": "📅 **Enter date in format `DD.MM.YYYY`**\n\n📌 **Example:** `15.10.2026`",
        "date_invalid": "❌ **Invalid date format.**\n\n💡 Correct format: `DD.MM.YYYY`\n📌 Example: `15.10.2026`",
        "welcome_back": "👋 **Welcome back!**\n\n🎓 **Your group:** {group}\n\n🎯 **Choose an action:**",
        "reset_success": "🔄 **Data reset!**\n\n🎯 Let's start over.\n\n🌍 **Choose language:**",
        "help_message": (
            "❓ **Help**\n\n"
            "📚 **Main commands:**\n"
            "• `/start` — start working with the bot\n"
            "• `/reset` — reset settings and start over\n"
            "• `/groups` — show all BFU groups\n"
            "• `/help` — show this message\n\n"
            "🆘 **Need help?**\n"
            "Contact: @alexa_ash_avery"
        ),
    }
}


def t(lang: str, key: str, **kwargs) -> str:
    # Если ключа нет в выбранном языке, пробуем взять из русского (для fallback)
    text = TEXTS.get(lang, TEXTS["ru"]).get(key, TEXTS["ru"].get(key, key))
    return text.format(**kwargs) if kwargs else text
