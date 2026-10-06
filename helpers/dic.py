from helpers.json_helper import get
from config.app import DICTIONARY_PATH

def text(key: str) -> str | None:
    return get(DICTIONARY_PATH, key)
