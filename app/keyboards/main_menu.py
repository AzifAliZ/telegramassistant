from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu():
    keyboard = [
        [
            InlineKeyboardButton(
                "💻 Web Development",
                callback_data="web_development"
            )
        ],
        [
            InlineKeyboardButton(
                "📱 App Development",
                callback_data="app_development"
            )
        ],
        [
            InlineKeyboardButton(
                "🤖 AI / ML",
                callback_data="ai_ml"
            )
        ],
        [
            InlineKeyboardButton(
                "🔐 Cyber Security",
                callback_data="cyber_security"
            )
        ],
        [
            InlineKeyboardButton(
                "💼 Software Services",
                callback_data="software_services"
            )
        ],
        [
            InlineKeyboardButton(
                "👤 About Me",
                callback_data="about_me"
            )
        ],
        [
            InlineKeyboardButton(
                "📞 Contact",
                callback_data="contact"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)