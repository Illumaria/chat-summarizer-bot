import logging

from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, PicklePersistence, Updater)

from src.constants import API_TOKEN, HEROKU_APP_NAME, PORT
from src.utils import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    if "history" not in context.user_data:
        context.user_data["history"] = []
    update.message.reply_text("Saving message history...")


def show_history(update: Update, context: CallbackContext) -> None:
    """Show history accumulated from reset to this moment."""
    update.message.reply_text(context.user_data["history"])


def save_history(update: Update, context: CallbackContext) -> None:
    """Save the user message to message history."""
    msg_id = update.message.message_id
    msg_time = update.message.date.strftime("%T")
    msg_text = update.message.text
    context.user_data["history"].append((msg_id, msg_time, msg_text))


def clear_history(update: Update, context: CallbackContext) -> None:
    """Clear the message history."""
    context.user_data["history"] = []


def main() -> None:
    """Start the bot."""
    persistence = PicklePersistence(filename="message_history")
    updater = Updater(API_TOKEN, persistence=persistence)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("history", show_history))
    dispatcher.add_handler(CommandHandler("reset", clear_history))

    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, save_history)
    )

    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=API_TOKEN,
        webhook_url=HEROKU_APP_NAME + API_TOKEN
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
