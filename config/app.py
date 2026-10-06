import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
MENU_CONFIG_PATH = os.environ["MENU_CONFIG_PATH"]
BOT_NAME = os.environ["BOT_NAME"]
BOT_SESSION_NAME = "session_" + BOT_NAME
PLACES_PATH = os.environ["PLACES_PATH"]
DICTIONARY_PATH = os.environ["DICTIONARY_PATH"]
BOT_BUTTON_MENU_COMMAND = "/menu@" + BOT_NAME
GIFTS_PATH = os.environ["GIFTS_PATH"]