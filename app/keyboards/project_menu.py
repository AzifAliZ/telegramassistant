from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def project_service_menu():

    keyboard = [
        [
            InlineKeyboardButton(
                "💻 Website",
                callback_data="project_website"
            )
        ],
        [
            InlineKeyboardButton(
                "📱 Mobile App",
                callback_data="project_mobile"
            )
        ],
        [
            InlineKeyboardButton(
                "🤖 AI / ML",
                callback_data="project_ai"
            )
        ],
        [
            InlineKeyboardButton(
                "🔐 Cyber Security",
                callback_data="project_security"
            )
        ],
        [
            InlineKeyboardButton(
                "💼 Custom Software",
                callback_data="project_software"
            )
        ],
        [
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data="cancel_project"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)