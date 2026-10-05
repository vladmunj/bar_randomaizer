import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = int(os.environ["CHAT_ID"])
GENERAL_TOPIC_ID = 1
BOT_SESSION_NAME = 'yankee_shishes_bot'
BOT_COMMAND = '/r@yankee_shishes_bot'
BOT_REMOVE_COMMAND = '/d'
BOT_RANDOM_PLACE_TEXT = os.environ["RANDOM_PLACE_TEXT"]
PLACES_PATH="places.json"
WISHLIST_PATH="wishlist.json"
BOT_WISHLIST_ADD_COMMAND = '/wa@yankee_shishes_bot'
BOT_WISHLIST_EMPTY_TEXT = os.environ["WISHLIST_EMPTY"]
BOT_WISHLIST_ADDED_TEXT = os.environ["WISHLIST_ADDED"]
BOT_WISHLISH_EXISTS_TEXT = os.environ["WISHLISH_EXISTS"]
BOT_WISHLIST_LIST_COMMAND = '/wl@yankee_shishes_bot'