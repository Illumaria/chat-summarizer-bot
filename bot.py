import logging
from typing import Any, List

from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    PicklePersistence,
    Updater,
)

from src.constants import API_TOKEN, GCLOUD_APP_NAME, PORT
from src.crud_operations import (
    create_session,
    create_table,
    delete_messages,
    get_messages,
    set_message,
    update_message,
)
from src.ranker import textrank
from src.utils import merge_same_author_messages, prettify, setup_logging

setup_logging()
logger = logging.getLogger(__name__)
session = create_session()


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    create_table(session)
    update.message.reply_text("Saving message history...")


def show_history(update: Update, context: CallbackContext) -> None:
    """Show history accumulated from reset to this moment."""
    chat_id = str(update.message.chat_id)
    msg_date = update.message.date.date().isoformat()
    history: List[Any] = get_messages(session, chat_id=chat_id, msg_date=msg_date)
    merged_history: List[Any] = merge_same_author_messages(history)
    top_message_indices: List[int] = textrank([x.msg_text.lower() for x in merged_history])
    summary: List[Any] = [merged_history[i] for i in top_message_indices]
    pretty_summary: str = prettify(summary)
    update.message.reply_text(pretty_summary)


def save_history(update: Update, context: CallbackContext) -> None:
    """Save the user message to message history."""
    if update.message is not None:
        set_message(session, update.message)
    elif update.edited_message is not None:
        update_message(session, update.edited_message)


def clear_history(update: Update, context: CallbackContext) -> None:
    """Clear the message history."""
    chat_id = str(update.message.chat_id)
    msg_date = update.message.date.date().isoformat()
    delete_messages(session, chat_id=chat_id, msg_date=msg_date)


def main() -> None:
    """Start the bot."""
    persistence = PicklePersistence(filename="message_history")
    updater = Updater(API_TOKEN, persistence=persistence)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start, run_async=True))
    dispatcher.add_handler(CommandHandler("history", show_history, run_async=True))
    dispatcher.add_handler(CommandHandler("reset", clear_history, run_async=True))

    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, save_history, run_async=True)
    )

    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=API_TOKEN,
        webhook_url=GCLOUD_APP_NAME + API_TOKEN,
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
