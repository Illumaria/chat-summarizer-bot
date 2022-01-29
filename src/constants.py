import os

from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
PORT = int(os.getenv("PORT", 5000))
HEROKU_APP_NAME = ""
