# version.py

# Текущая версия бота
BOT_VERSION = "1.1.0"

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
            "🆘 Нашли ошибку? Напишите: @alexa_ash_avery"
        ),
        "en": (
            "🎉 <b>Version 1.0.0 — First release!</b>\n\n"
            "✅ Schedule for today / tomorrow / the week\n"
            "✅ Choose any date\n"
            "✅ Bilingual interface (🇷🇺/🇬🇧)\n"
            "✅ Handy menu buttons\n"
            "✅ Link to the website with the full list of groups\n\n"
            "🆘 Found a bug? Contact: @alexa_ash_avery"
        ),
    },
    "1.1.0": {
        "ru": (
            "🚀 <b>Версия 1.1.0</b>\n\n"
            "✅ Расписание на <b>любую дату</b> — из прошлого и из будущего\n"
            "✅ Дни недели на твоём языке\n"
            "✅ Все сообщения бота на русском и английском\n"
            "✅ Исправлены ошибки и ускорена загрузка расписания\n\n"
            "🆘 Нашли ошибку? Напишите в супер-поддержку: @alexa_ash_avery"
        ),
        "en": (
            "🚀 <b>Version 1.1.0</b>\n\n"
            "✅ Schedule for <b>any date</b> — past or future\n"
            "✅ Weekdays in your language\n"
            "✅ All bot messages in both Russian and English\n"
            "✅ Bug fixes and faster schedule loading\n\n"
            "🆘 Found a bug? Contact our super support: @alexa_ash_avery"
        ),
    },
}


def changelog_text(version: str, lang: str) -> str:
    """Текст изменений версии на нужном языке (если нет, то русский)."""
    entry = CHANGELOG[version]
    return entry.get(lang) or entry["ru"]
