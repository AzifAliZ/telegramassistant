from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def web_development_menu():
    keyboard = [
        [
            InlineKeyboardButton(
                "🌐 Website Development",
                callback_data="websites"
            )
        ],
        [
            InlineKeyboardButton(
                "⚛️ React Development",
                callback_data="react"
            )
        ],
        [
            InlineKeyboardButton(
                "▲ Next.js Development",
                callback_data="nextjs"
            )
        ],
        [
            InlineKeyboardButton(
                "🐍 Django Development",
                callback_data="django"
            )
        ],
        [
            InlineKeyboardButton(
                "🛒 E-commerce",
                callback_data="ecommerce"
            )
        ],
        [
    InlineKeyboardButton(
        "📩 Request a Project",
        callback_data="request_project"
    )
],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="main_menu"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)