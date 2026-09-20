from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.config import CONTACT_PHONE


def contact_menu():

    whatsapp_url = f"https://wa.me/{CONTACT_PHONE}"

    keyboard = [
        [
            InlineKeyboardButton(
                "💬 WhatsApp",
                url=whatsapp_url
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