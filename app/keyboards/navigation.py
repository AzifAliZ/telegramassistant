from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def navigation_menu(back_callback="main_menu"):
    keyboard = [
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data=back_callback
            ),
            InlineKeyboardButton(
                "🏠 Main Menu",
                callback_data="main_menu"
            ),
        ]
    ]

    return InlineKeyboardMarkup(keyboard)