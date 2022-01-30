import os

API_TOKEN = os.environ.get("API_TOKEN")
PORT = int(os.environ.get("PORT", 5000))
HEROKU_APP_NAME = "https://chat-summarizer-bot.herokuapp.com/"
