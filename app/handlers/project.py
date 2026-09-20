from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
from app.database.db import save_project_request
from app.keyboards.project_menu import project_service_menu


NAME, SERVICE, REQUIREMENT, CONTACT = range(4)


async def start_project(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.callback_query.answer()

    await update.callback_query.message.reply_text(
        "📩 Project Request\n\n"
        "Let's collect a few details.\n\n"
        "What is your name?"
    )

    return NAME


async def get_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["name"] = update.message.text

    await update.message.reply_text(
        "Thanks! 👍\n\n"
        "What type of project are you interested in?",
        reply_markup=project_service_menu()
    )

    return SERVICE


async def get_service(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    service_map = {
        "project_website": "Website",
        "project_mobile": "Mobile App",
        "project_ai": "AI / ML",
        "project_security": "Cyber Security",
        "project_software": "Custom Software",
    }

    if query.data == "cancel_project":

        await query.edit_message_text(
            "❌ Project request cancelled."
        )

        return ConversationHandler.END

    service = service_map.get(query.data)

    context.user_data["service"] = service

    await query.edit_message_text(
        f"Selected: {service}\n\n"
        "Tell me briefly about your project.\n\n"
        "For example:\n"
        "I need a business website with an "
        "admin panel and contact form."
    )

    return REQUIREMENT


async def get_requirement(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["requirement"] = update.message.text

    await update.message.reply_text(
        "Almost done! 👍\n\n"
        "How can I contact you?\n\n"
        "You can provide your phone number,\n"
        "WhatsApp number or email."
    )

    return CONTACT


async def get_contact(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["contact"] = update.message.text

    name = context.user_data["name"]
    service = context.user_data["service"]
    requirement = context.user_data["requirement"]
    contact = context.user_data["contact"]

    telegram_user = update.effective_user

    request_id = save_project_request(
        name=name,
        service=service,
        requirement=requirement,
        contact=contact,
        telegram_user_id=telegram_user.id,
        telegram_username=telegram_user.username,
    )

    summary = f"""
✅ Project Request Submitted!

Reference ID: #{request_id}

👤 Name:
{name}

💼 Service:
{service}

📝 Requirement:
{requirement}

📞 Contact:
{contact}

Thank you! I'll review your request.
"""

    await update.message.reply_text(summary)

    context.user_data.clear()

    return ConversationHandler.END


async def cancel_project(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data.clear()

    await update.message.reply_text(
        "❌ Project request cancelled."
    )

    return ConversationHandler.END