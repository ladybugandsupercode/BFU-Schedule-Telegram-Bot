TEXTS = {
    "ru": {
        "welcome": (
            "👋 <b>Привет! Я — бот расписания БФУ им. И. Канта.</b>\n\n"
            "🎓 <b>Я помогу тебе:</b>\n"
            "• 📅 Узнать расписание на сегодня/завтра\n"
            "• 🗓 Посмотреть расписание на всю неделю\n"
            "• 📆 Найти пары на любую дату\n"
            "• 📋 Получить список всех групп БФУ\n\n"
            "🎯 <b>Как пользоваться:</b>\n"
            "1️⃣ Выбери язык\n"
            "2️⃣ Введи номер своей группы\n"
            "3️⃣ Нажимай кнопки меню для просмотра расписания\n\n"
            "🌟 <b>Давай начнём!</b> Сначала выбери язык:"
        ),
        "after_language": (
            "✅ <b>Отлично!</b>\n\n"
            "🎯 <b>Что дальше?</b>\n\n"
            "📝 <b>Выбери действие:</b>"
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
            "Напиши /groups — покажу список всех специальностей БФУ\n\n"
            "⚠️ <b>Важно:</b> Вводи группу <b>точно</b> как в зачётке!\n\n"
            "👇 <b>Введи свою группу:</b>"
        ),
        "group_saved": "✅ <b>Группа {group} сохранена!</b>\n\n🎯 Теперь выбери, что показать:",
        "group_invalid": (
            "❌ <b>Группа указана неверно.</b>\n\n"
            "💡 Проверь формат: <code>03_ФИИТ_26_02</code>\n"
            "📋 Или напиши /groups для списка специальностей\n\n"
            "👇 <b>Попробуй ещё раз:</b>"
        ),
        "group_not_found": (
            "❌ <b>Группа не найдена в базе БФУ.</b>\n\n"
            "💡 Возможно, ты ошибся в названии.\n"
            "📋 Напиши /groups — покажу список всех групп\n\n"
            "🆘 <b>Если вашей группы нет в списке</b> или она не отображается:\n"
            "Напишите в поддержку: @alexa_ash_avery\n\n"
            "👇 <b>Попробуй ввести группу ещё раз:</b>"
        ),
        "fetch_error": (
            "❌ <b>Не удалось получить расписание.</b>\n\n"
            "💡 Возможно, группа указана неверно или сайт БФУ временно недоступен.\n"
            "📋 Напиши /groups для проверки списка групп\n\n"
            "🆘 <b>Если проблема не решается:</b>\n"
            "Напишите в поддержку: @your_username"
        ),
        "choose_lang": "🌍 <b>Выбери язык / Choose language:</b>",
        "lang_set": "✅ <b>Язык установлен: Русский</b>",
        "no_classes": "🎉 <b>Пар нет — можно отдыхать!</b>",
        "error_schedule": (
            "❌ <b>Ошибка получения расписания.</b>\n\n"
            "💡 Попробуй позже или проверь группу командой /groups\n\n"
            "🆘 <b>Если проблема сохраняется:</b>\n"
            "Напишите в поддержку: @your_username"
        ),
        "settings": (
            "⚙️ <b>Настройки</b>\n\n"
            "📚 <b>Текущая группа:</b> {group}\n\n"
            "👇 <b>Введи новый номер группы:</b>"
        ),
        "today": "📅 Сегодня",
        "tomorrow": "📆 Завтра",
        "week": "🗓 На неделю",
        "custom_date": "📆 Выбрать дату",
        "settings_btn": "⚙️ Настройки",
        "language_btn": "🌍 Язык",
        "groups_btn": "📋 Список групп",
        "help_btn": "❓ Помощь",
        "enter_date": "📅 <b>Введи дату в формате <code>ДД.ММ.ГГГГ</code></b>\n\n📌 <b>Пример:</b> <code>15.10.2026</code>",
        "date_invalid": "❌ <b>Неверный формат даты.</b>\n\n💡 Правильный формат: <code>ДД.ММ.ГГГГ</code>\n📌 Пример: <code>15.10.2026</code>",
        "welcome_back": (
            "👋 <b>С возвращением!</b>\n\n"
            "🎓 <b>Твоя группа:</b> {group}\n\n"
            "🎯 <b>Выбери действие:</b>"
        ),
        "reset_success": "🔄 <b>Данные сброшены!</b>\n\n🎯 Давай начнём заново.\n\n🌍 <b>Выбери язык:</b>",
        "help_message": (
            "❓ <b>Помощь</b>\n\n"
            "📚 <b>Основные команды:</b>\n"
            "• /start — начать работу с ботом\n"
            "• /reset — сбросить настройки и начать заново\n"
            "• /groups — показать список всех групп БФУ\n"
            "• /help — показать это сообщение\n\n"
            "🎯 <b>Кнопки меню:</b>\n"
            "• 📅 Сегодня — расписание на сегодня\n"
            "• 📆 Завтра — расписание на завтра\n"
            "• 🗓 На неделю — расписание на всю неделю\n"
            "• 📆 Выбрать дату — расписание на конкретную дату\n"
            "• ⚙️ Настройки — сменить группу\n"
            "• 🌍 Язык — сменить язык\n"
            "• 📋 Список групп — показать все специальности\n\n"
            "🆘 <b>Нужна помощь?</b>\n"
            "Напишите в поддержку: @your_username"
        ),
    },
    "en": {
        "welcome": (
            "👋 <b>Hello! I'm the BFU Im. Kant schedule bot.</b>\n\n"
            "🎓 <b>I'll help you:</b>\n"
            "• 📅 Check today's/tomorrow's schedule\n"
            "• 🗓 View the full week schedule\n"
            "• 📆 Find classes for any specific date\n"
            "• 📋 Get a list of all BFU groups\n\n"
            "🎯 <b>How to use:</b>\n"
            "1️⃣ Choose your language\n"
            "2️⃣ Enter your group number\n"
            "3️⃣ Use menu buttons to view schedules\n\n"
            "🌟 <b>Let's start!</b> First, choose your language:"
        ),
        "after_language": (
            "✅ <b>Great!</b>\n\n"
            "🎯 <b>What's next?</b>\n\n"
            "📝 <b>Choose an action:</b>"
        ),
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
            "Type /groups — I'll show all BFU programs\n\n"
            "⚠️ <b>Important:</b> Enter the group <b>exactly</b> as in your student ID!\n\n"
            "👇 <b>Enter your group:</b>"
        ),
        "group_saved": "✅ <b>Group {group} saved!</b>\n\n🎯 Now choose what to show:",
        "group_invalid": (
            "❌ <b>Invalid group number.</b>\n\n"
            "💡 Check the format: <code>03_ФИИТ_26_02</code>\n"
            "📋 Or type /groups for the list of programs\n\n"
            "👇 <b>Try again:</b>"
        ),
        "group_not_found": (
            "❌ <b>Group not found in BFU database.</b>\n\n"
            "💡 You might have made a typo.\n"
            "📋 Type /groups to see all groups\n\n"
            "🆘 <b>If your group is not in the list</b> or doesn't appear:\n"
            "Contact support: @your_username\n\n"
            "👇 <b>Try entering the group again:</b>"
        ),
        "fetch_error": (
            "❌ <b>Could not fetch schedule.</b>\n\n"
            "💡 The group might be incorrect or BFU website is temporarily unavailable.\n"
            "📋 Type /groups to verify the group list\n\n"
            "🆘 <b>If the problem persists:</b>\n"
            "Contact support: @your_username"
        ),
        "choose_lang": "🌍 <b>Choose language / Выбери язык:</b>",
        "lang_set": "✅ <b>Language set: English</b>",
        "no_classes": "🎉 <b>No classes today — enjoy your free time!</b>",
        "error_schedule": (
            "❌ <b>Error fetching schedule.</b>\n\n"
            "💡 Try again later or verify the group with /groups\n\n"
            "🆘 <b>If the problem persists:</b>\n"
            "Contact support: @your_username"
        ),
        "settings": (
            "⚙️ <b>Settings</b>\n\n"
            "📚 <b>Current group:</b> {group}\n\n"
            "👇 <b>Enter new group number:</b>"
        ),
        "today": "📅 Today",
        "tomorrow": "📆 Tomorrow",
        "week": "🗓 Week",
        "custom_date": "📆 Custom date",
        "settings_btn": "⚙️ Settings",
        "language_btn": "🌍 Language",
        "groups_btn": "📋 Group list",
        "help_btn": "❓ Help",
        "enter_date": "📅 <b>Enter date in format <code>DD.MM.YYYY</code></b>\n\n📌 <b>Example:</b> <code>15.10.2026</code>",
        "date_invalid": "❌ <b>Invalid date format.</b>\n\n💡 Correct format: <code>DD.MM.YYYY</code>\n📌 Example: <code>15.10.2026</code>",
        "welcome_back": (
            "👋 <b>Welcome back!</b>\n\n"
            "🎓 <b>Your group:</b> {group}\n\n"
            "🎯 <b>Choose an action:</b>"
        ),
        "reset_success": "🔄 <b>Data reset!</b>\n\n🎯 Let's start over.\n\n🌍 <b>Choose language:</b>",
        "help_message": (
            "❓ <b>Help</b>\n\n"
            "📚 <b>Main commands:</b>\n"
            "• /start — start working with the bot\n"
            "• /reset — reset settings and start over\n"
            "• /groups — show all BFU groups\n"
            "• /help — show this message\n\n"
            "🎯 <b>Menu buttons:</b>\n"
            "• 📅 Today — today's schedule\n"
            "• 📆 Tomorrow — tomorrow's schedule\n"
            "• 🗓 Week — full week schedule\n"
            "• 📆 Custom date — schedule for a specific date\n"
            "• ⚙️ Settings — change group\n"
            "• 🌍 Language — change language\n"
            "• 📋 Group list — show all programs\n\n"
            "🆘 <b>Need help?</b>\n"
            "Contact support: @your_username"
        ),
    }
}


def t(lang: str, key: str, **kwargs) -> str:
    text = TEXTS.get(lang, TEXTS["ru"]).get(key, key)
    return text.format(**kwargs) if kwargs else text
