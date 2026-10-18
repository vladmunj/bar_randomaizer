from helpers.json_helper import get
import json
from config.app import (
    DICTIONARY_PATH,
    LOCALES_PATH
)

def text(key: str) -> str | None:
    return get(DICTIONARY_PATH, key)

def locales() -> list[str]:
    with LOCALES_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)