TEXTS = {
    "ru": {
        "welcome_bilingual": (
            "👋 <b>Привет! / Hello!</b>\n\n"
            "🎓 <b>Я — бот расписания БФУ им. И. Канта.</b>\n"
            "🎓 <b>I am the BFU Im. Kant schedule bot.</b>\n\n"
            "📋 <b>Как пользоваться / How to use:</b>\n"
            "   1️⃣ Выбери язык / Choose language\n"
            "   2️⃣ Введи номер группы / Enter group number\n"
            "   3️⃣ Смотри расписание / Check schedule\n\n"
            "⚙️ <b>Кнопки меню / Menu buttons:</b>\n"
            "   📅 <b>Сегодня / Today</b> — пары на сегодня\n"
            "   📆 <b>Завтра / Tomorrow</b> — пары на завтра\n"
            "   🗓 <b>На неделю / Week</b> — расписание на 7 дней\n"
            "   📆 <b>Дата / Date</b> — расписание на конкретный день\n"
            "   ⚙️ <b>Настройки / Settings</b> — сменить группу\n"
            "   🌍 <b>Язык / Language</b> — сменить язык\n"
            "   📋 <b>Группы / Groups</b> — список всех специальностей\n"
            "   ❓ <b>Помощь / Help</b> — подробный гайд\n\n"
            "   🆘 <b>Нужна помощь? / Need help?</b>\n"
            "Если у вас есть предложения по улучшению или бот работает некорректно, напишите в нашу супер-поддержку: @alexa_ash_avery\n\n"
            "👇 <b>Выберите язык / Choose language:</b>"
        ),
        "after_language": (
            "✅ <b>Отлично! / Great!</b>\n\n"
            "👇 <b>Выберите действие / Choose an action:</b>"
        ),
        "group_saved": "✅ <b>Группа {groups_text} сохранена!</b>\n\n🎯 Теперь выбери, что показать:",
        "group_invalid": (
            "❌ <b>Группа указана неверно.</b>\n\n"
            "💡 Проверь формат: <code>03_ФИИТ_26_02</code>\n"
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
        "choose_lang": "🌍 <b>Выбери язык / Choose language:</b>",
        "lang_set": "✅ <b>Язык установлен: Русский</b>",
        "no_classes": "🎉 <b>Пар нет — можно отдыхать!</b>",
        "error_schedule": (
            "❌ <b>Ошибка получения расписания.</b>\n\n"
            "🆘 Если проблема сохраняется, напиши: @alexa_ash_avery"
        ),
        "settings": (
            "⚙️ <b>Настройки</b>\n\n"
            "📚 <b>Текущая группа:</b> {groups_text}\n\n"
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
            "🎓 <b>Твоя группа:</b> {groups_text}\n\n"
            "🎯 <b>Выбери действие:</b>"
        ),
        "reset_success": "🔄 <b>Данные сброшены!</b>\n\n👇 <b>Выберите язык для продолжения:</b>",
        "help_message": (
            "❓ <b>Помощь / Help</b>\n\n"
            "📚 <b>Основные команды:</b>\n"
            "   • <code>/start</code> — начать работу с ботом\n"
            "   • <code>/reset</code> — сбросить настройки\n"
            "   • <code>/groups</code> — список всех групп БФУ\n"
            "   • <code>/help</code> — показать это сообщение\n\n"
            "🆘 <b>Нужна помощь?</b>\n"
            "Напишите супер-поддержке: @alexa_ash_avery"
        ),
        "groups_text": (
            "📋 <b>Список всех групп БФУ</b>\n\n"
            "🔗 <b>Посмотри на сайте:</b> https://schedule.kantiana.ru\n\n"
            "💡 <b>Как найти свою группу:</b>\n"
            "   1️⃣ Открой сайт\n"
            "   2️⃣ Выбери свой институт/колледж\n"
            "   3️⃣ Найди направление и курс\n"
            "   4️⃣ Скопируй название группы (например, <code>03_ФИИТ_26_2</code>)\n"
            "   5️⃣ Введи его сюда\n\n"
            "🆘 <b>Не можешь найти?</b>\n"
            "Напиши супер-поддержке: @alexa_ash_avery"
        ),
    },
    "en": {
        "after_language": "✅ <b>Great!</b>\n\n👇 <b>Choose an action:</b>",
        "group_saved": "✅ <b>Group {groups_text} saved!</b>\n\n🎯 Now choose what to show:",
        "group_invalid": "❌ <b>Invalid group number.</b>\n\n💡 Check the format: <code>03_ФИИТ_26_02</code>\n👇 <b>Try again:</b>",
        "group_not_found": "❌ <b>Group not found in BFU database.</b>\n\n🆘 If you have any suggestions for improvement or if the bot is not working correctly, please reach out to our super-support team: @alexa_ash_avery\n\n👇 <b>Try entering the group again:</b>",
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
        "welcome_back": "👋 <b>Welcome back!</b>\n\n🎓 <b>Your group:</b> {groups_text}\n\n🎯 <b>Choose an action:</b>",
        "reset_success": "🔄 <b>Data reset!</b>\n\n👇 <b>Choose language to continue:</b>",
        "help_message": (
            "❓ <b>Help</b>\n\n"
            "📚 <b>Main commands:</b>\n"
            "   • <code>/start</code> — start working with the bot\n"
            "   • <code>/reset</code> — reset settings\n"
            "   • <code>/groups</code> — show all BFU groups\n"
            "   • <code>/help</code> — show this message\n\n"
            "🆘 <b>Need help?</b>\n"
            "Contact our super-support: @alexa_ash_avery"
        ),
        "groups_text": (
            "📋 <b>List of all BFU groups</b>\n\n"
            "🔗 <b>Check the website:</b> https://schedule.kantiana.ru/\n\n"
            "💡 <b>How to find your group:</b>\n"
            "   1️⃣ Open the website\n"
            "   2️⃣ Choose your institute/college\n"
            "   3️⃣ Find your program and year\n"
            "   4️⃣ Copy the group name (e.g., <code>03_ФИИТ_26_2</code>)\n"
            "   5️⃣ Enter it here\n\n"
            "🆘 <b>Can't find it?</b>\n"
            "Contact our super-support: @alexa_ash_avery"
        ),
    }
}

def t(lang: str, key: str, **kwargs) -> str:
    text = TEXTS.get(lang, TEXTS["ru"]).get(key, TEXTS["ru"].get(key, key))
    return text.format(**kwargs) if kwargs else text
