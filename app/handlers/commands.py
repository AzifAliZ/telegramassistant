from telegram import Update
from telegram.ext import ContextTypes

from app.keyboards.main_menu import main_menu
from app.responses.messages import WELCOME_MESSAGE


async def menu_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        text=WELCOME_MESSAGE,
        reply_markup=main_menu()
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    help_message = """
ℹ️ Help

You can use the buttons below to
explore my services.

Available commands:

/start - Start the bot
/menu - Open the main menu
/help - Show this help message

You can also type a message and
I'll try to guide you.
"""

    await update.message.reply_text(
        text=help_message,
        reply_markup=main_menu()
    )