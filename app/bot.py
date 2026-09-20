from app.database.db import init_database
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)
from app.handlers.admin import (
    leads_command,
    lead_command,
    admin_lead_callback,
    stats_command,
    export_command,
)
from app.config import BOT_TOKEN
from app.keyboards.main_menu import main_menu
from app.responses.messages import WELCOME_MESSAGE

# Handlers
from app.handlers.project import (
    start_project,
    get_name,
    get_service,
    get_requirement,
    get_contact,
    cancel_project,
    NAME,
    SERVICE,
    REQUIREMENT,
    CONTACT,
)
from app.handlers.menu import menu_callback
from app.handlers.commands import menu_command, help_command
from app.handlers.fallback import fallback
from app.handlers.admin import leads_command, lead_command, admin_lead_callback
from app.handlers.errors import error_handler


# =========================
# START COMMAND
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=WELCOME_MESSAGE,
        reply_markup=main_menu()
    )


def create_bot():
    init_database()

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .connect_timeout(30)
        .read_timeout(30)
        .write_timeout(30)
        .pool_timeout(30)
        .build()
    )

    # =========================
    # COMMANDS
    # =========================
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("leads", leads_command))
    application.add_handler(CommandHandler("lead", lead_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("export", export_command))
    

    # =========================
    # ADMIN CALLBACKS
    # =========================
    application.add_handler(
    CallbackQueryHandler(
        admin_lead_callback,
        pattern=r"^(view_lead_|status_lead_|set_status_|cancel_status_|delete_lead_|confirm_delete_|cancel_delete_|admin_leads)"
    )
)

    # =========================
    # PROJECT CONVERSATION
    # =========================
    project_conversation = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_project, pattern="^request_project$")
        ],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            SERVICE: [CallbackQueryHandler(get_service, pattern="^project_")],
            REQUIREMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_requirement)],
            CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_contact)],
        },
        fallbacks=[CommandHandler("cancel", cancel_project)],
    )
    application.add_handler(project_conversation)

    # =========================
    # INLINE BUTTONS
    # =========================
    application.add_handler(CallbackQueryHandler(menu_callback))

    # =========================
    # TEXT FALLBACK
    # =========================
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))

    # =========================
# ERROR HANDLER
# =========================
    application.add_error_handler(error_handler)

    return application
