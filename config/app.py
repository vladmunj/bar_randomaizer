import os
from dotenv import load_dotenv
from pathlib import Path

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
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
APP_LOCALE = os.getenv("APP_LOCALE")
TMDB_SOURCE_TYPE_TV = "tv"
TMDB_SOURCE_TYPE_MOVIE = "movie"
TMDB_MOVIE_TYPES = [TMDB_SOURCE_TYPE_MOVIE, TMDB_SOURCE_TYPE_TV]
TMDB_MIN_RATING = os.getenv("TMDB_MIN_RATING")
DEFAULT_POSTER_RUS = Path(__file__).resolve().parent.parent/"assets"/"no_poster_rus.jpg"
LOCALES_PATH = Path(__file__).resolve().parent.parent/"config"/"locales.json"
TMDB_MAX_OVERVIEW_LENGTH = 700
KINOGO_SEARCH_URL = "https://kinogo.family/search/"
KINOPOISK_SEARCH_URL = "https://www.kinopoisk.ru/new-search/?text="
MOVIE_LINKS_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0.0.0 Safari/537.36"
    )
}