import logging

from telegram import Update
from telegram.ext import ContextTypes


logger = logging.getLogger(__name__)


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):
    logger.error(
        "Exception while processing an update:",
        exc_info=context.error
    )

    # Try to inform the user when possible
    if isinstance(update, Update):

        if update.effective_message:

            try:
                await update.effective_message.reply_text(
                    "⚠️ Something went wrong while processing your request.\n"
                    "Please try again."
                )
            except Exception:
                pass