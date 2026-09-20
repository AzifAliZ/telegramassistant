from telegram import Update
from telegram.ext import ContextTypes

from app.keyboards.main_menu import main_menu
from app.keyboards.services_menu import web_development_menu
from app.keyboards.contact_menu import contact_menu
from app.keyboards.navigation import navigation_menu

from app.responses.messages import (
    WELCOME_MESSAGE,
    WEB_DEVELOPMENT_MENU_MESSAGE,
)

from app.responses.services import (
    WEBSITE_MESSAGE,
    REACT_MESSAGE,
    NEXTJS_MESSAGE,
    DJANGO_MESSAGE,
    ECOMMERCE_MESSAGE,
)

from app.responses.main_menu_responses import (
    APP_DEVELOPMENT_MESSAGE,
    AI_ML_MESSAGE,
    CYBER_SECURITY_MESSAGE,
    SOFTWARE_SERVICES_MESSAGE,
    ABOUT_ME_MESSAGE,
    CONTACT_MESSAGE,
)


async def menu_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    # =================================
    # WEB DEVELOPMENT
    # =================================

    if query.data == "web_development":

        await query.edit_message_text(
            text=WEB_DEVELOPMENT_MENU_MESSAGE,
            reply_markup=web_development_menu()
        )

    elif query.data == "websites":

        await query.edit_message_text(
            text=WEBSITE_MESSAGE,
            reply_markup=navigation_menu(
                "web_development"
            )
        )

    elif query.data == "react":

        await query.edit_message_text(
            text=REACT_MESSAGE,
            reply_markup=navigation_menu(
                "web_development"
            )
        )

    elif query.data == "nextjs":

        await query.edit_message_text(
            text=NEXTJS_MESSAGE,
            reply_markup=navigation_menu(
                "web_development"
            )
        )

    elif query.data == "django":

        await query.edit_message_text(
            text=DJANGO_MESSAGE,
            reply_markup=navigation_menu(
                "web_development"
            )
        )

    elif query.data == "ecommerce":

        await query.edit_message_text(
            text=ECOMMERCE_MESSAGE,
            reply_markup=navigation_menu(
                "web_development"
            )
        )

    # =================================
    # MAIN MENU SERVICES
    # =================================

    elif query.data == "app_development":

        await query.edit_message_text(
            text=APP_DEVELOPMENT_MESSAGE,
            reply_markup=navigation_menu()
        )

    elif query.data == "ai_ml":

        await query.edit_message_text(
            text=AI_ML_MESSAGE,
            reply_markup=navigation_menu()
        )

    elif query.data == "cyber_security":

        await query.edit_message_text(
            text=CYBER_SECURITY_MESSAGE,
            reply_markup=navigation_menu()
        )

    elif query.data == "software_services":

        await query.edit_message_text(
            text=SOFTWARE_SERVICES_MESSAGE,
            reply_markup=navigation_menu()
        )

    elif query.data == "about_me":

        await query.edit_message_text(
            text=ABOUT_ME_MESSAGE,
            reply_markup=navigation_menu()
        )

    # =================================
    # CONTACT
    # =================================

    elif query.data == "contact":

        await query.edit_message_text(
            text=CONTACT_MESSAGE,
            reply_markup=contact_menu()
        )

    # =================================
    # MAIN MENU
    # =================================

    elif query.data == "main_menu":

        await query.edit_message_text(
            text=WELCOME_MESSAGE,
            reply_markup=main_menu()
        )