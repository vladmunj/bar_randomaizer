from pathlib import Path
import re
import json
import random
from config.app import PLACES_PATH
from helpers.dic import text

PLACES_DATA = Path(PLACES_PATH)
URL_PATTERN = re.compile(
    r"https?://[^\s<>\]\)]+",
    re.IGNORECASE,
)

def load_links() -> list[str]:
    with PLACES_DATA.open("r", encoding = "utf-8") as file:
        links = json.load(file)
    return links

def random_link() -> str | None:
    links = load_links()
    if not links: return text("places_empty")
    return random.choice(links)

def extract_url(text: str) -> list[str] | None:
    if not text: return None
    try:
        return URL_PATTERN.findall(text)[0]
    except Exception:
        return None