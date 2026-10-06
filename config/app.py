import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
MENU_CONFIG_PATH = os.environ["MENU_CONFIG_PATH"]
BOT_SESSION_NAME = os.environ["BOT_SESSION_NAME"]
BOT_MENU_TITLE_TEXT = os.environ["BOT_MENU_TITLE"]
PLACES_PATH = os.environ["PLACES_PATH"]
BOT_RANDOM_PLACE_TEXT = os.environ["RANDOM_PLACE_TEXT"]