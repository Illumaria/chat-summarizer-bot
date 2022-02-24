import os

API_TOKEN = os.environ.get("API_TOKEN")
PORT = int(os.environ.get("WEBHOOK_PORT", 5000))

ASTRA_DB_KEYSPACE = "chat_summarizer_bot"
ASTRA_DB_TABLE_NAME = "messages"
ASTRA_DB_SCB_PATH = os.environ.get("ASTRA_DB_SCB_PATH")
ASTRA_DB_USERNAME = os.environ.get("ASTRA_DB_USERNAME")
ASTRA_DB_PASSWORD = os.environ.get("ASTRA_DB_PASSWORD")

GCLOUD_APP_NAME = "https://chat-summarizer-bot.lm.r.appspot.com"
