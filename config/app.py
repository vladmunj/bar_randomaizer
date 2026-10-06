import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
MENU_CONFIG_PATH = os.environ["MENU_CONFIG_PATH"]
BOT_SESSION_NAME = os.environ["BOT_SESSION_NAME"]
PLACES_PATH = os.environ["PLACES_PATH"]
DICTIONARY_PATH = os.environ["DICTIONARY_PATH"]