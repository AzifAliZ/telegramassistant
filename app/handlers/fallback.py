from telegram import Update
from telegram.ext import ContextTypes

from app.keyboards.main_menu import main_menu
from app.responses.rules import RULES


def detect_intent(message: str):
    """
    Find the first matching rule based on keywords.
    """

    message = message.lower().strip()

    for intent, keywords in RULES.items():

        for keyword in keywords:

            if keyword in message:
                return intent

    return None


async def fallback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = update.message.text

    intent = detect_intent(message)

    if intent == "greeting":

        response = """
👋 Hello!

Welcome to my Telegram Assistant.

What would you like to explore?
"""

    elif intent == "web_development":

        response = """
💻 Looking for web development?

I can help with websites and
web applications.

Please choose Web Development
from the menu to explore the options.
"""

    elif intent == "app_development":

        response = """
📱 Looking for app development?

I can help with mobile application
development.

Please select App Development
from the menu.
"""

    elif intent == "ai_ml":

        response = """
🤖 Interested in AI / ML?

Please select AI / ML from the
main menu to explore the available
services.
"""

    elif intent == "contact":

        response = """
📞 You can find my contact information
through the Contact section.
"""

    else:

        response = """
🤖 I'm currently a rule-based assistant.

I didn't quite understand that.

Please choose an option from the
menu below.
"""

    await update.message.reply_text(
        text=response,
        reply_markup=main_menu()
    )