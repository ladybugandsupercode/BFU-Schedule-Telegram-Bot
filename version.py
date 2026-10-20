# version.py

# Текущая версия бота
BOT_VERSION = "2.0.0"

# История изменений. Для каждой версии два текста: "ru" и "en".
# Новые версии добавляй в конец словаря (и меняй BOT_VERSION выше).
CHANGELOG = {
    "1.0.0": {
        "ru": (
            "🎉 <b>Версия 1.0.0 — Первый релиз!</b>\n\n"
            "✅ Просмотр расписания на сегодня/завтра/неделю\n"
            "✅ Выбор произвольной даты\n"
            "✅ Двуязычный интерфейс (🇷🇺/🇬🇧)\n"
            "✅ Удобные кнопки меню\n"
            "✅ Ссылка на сайт с полным списком групп\n\n"
        ),
        "en": (
            "🎉 <b>Version 1.0.0 — First release!</b>\n\n"
            "✅ Schedule for today / tomorrow / the week\n"
            "✅ Choose any date\n"
            "✅ Bilingual interface (🇷🇺/🇬🇧)\n"
            "✅ Handy menu buttons\n"
            "✅ Link to the website with the full list of groups\n\n"
        ),
    },
    "1.1.0": {
        "ru": (
            "🚀 <b>Версия 1.1.0</b>\n\n"
            "✅ Расписание на <b>любую дату</b> — из прошлого и из будущего\n"
            "✅ Дни недели на твоём языке\n"
            "✅ Все сообщения бота на русском и английском\n"
            "✅ Исправлены ошибки и ускорена загрузка расписания\n\n"
        ),
        "en": (
            "🚀 <b>Version 1.1.0</b>\n\n"
            "✅ Schedule for <b>any date</b> — past or future\n"
            "✅ Weekdays in your language\n"
            "✅ All bot messages in both Russian and English\n"
            "✅ Bug fixes and faster schedule loading\n\n"
        ),
    },
    "2.0.0": {
        "ru": (
            "🎊 <b>Версия 2.0.0 — Большое обновление!</b>\n\n"
            "✨ <b>Что нового:</b>\n"
            "   👨‍🏫 Полные ФИО преподавателей — теперь видно, кто ведёт пару\n"
            "   ➡️ Кнопка <b>«Следующая неделя»</b> — планирование вперёд\n"
            "   📜 Красивое оформление: пары в блоке «цитата» для удобства\n"
            "   🏫 <b>Кабинеты выделены жирным</b> — мгновенно находишь аудиторию\n"
            "   💖 Кнопка <b>«Поддержать разработчицу»</b> — спасибо за кофеёк;) \n\n"
            "🛠 Также исправлены некоторые ошибки.\n\n"
            "🆘 Нашли ошибку? Напишите в супер-поддержку: @alexa_ash_avery"
        ),
        "en": (
            "🎊 <b>Version 2.0.0 — Major update!</b>\n\n"
            "✨ <b>What's new:</b>\n"
            "   👨‍🏫 Full teacher names — now you see who teaches the class\n"
            "   ➡️ <b>«Next week»</b> button — plan ahead\n"
            "   📜 Beautiful formatting: lessons in a quote block for readability\n"
            "   🏫 <b>Rooms are bold</b> — instantly find your classroom\n"
            "   💖 <b>«Support the developer»</b> button — thanks for the coffee;) \n\n"
            "🛠 Also fixed some bugs.\n\n"
            "🆘 Found a bug? Contact our super-support: @alexa_ash_avery"
        ),
    },
}

def changelog_text(version: str, lang: str) -> str:
    """Текст изменений версии на нужном языке (если нет, то русский)."""
    entry = CHANGELOG[version]
    return entry.get(lang) or entry["ru"]
