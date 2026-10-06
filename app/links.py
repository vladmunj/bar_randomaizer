from pathlib import Path
import re
import json
import random
from config.app import PLACES_PATH

PLACES_DATA = Path(PLACES_PATH)
URL_PATTERN = re.compile(
    r"https?://2gis.kz[^\s<>\]\)]+",
    re.IGNORECASE,
)

def load_links() -> list[str]:
    with PLACES_DATA.open("r", encoding = "utf-8") as file:
        links = json.load(file)
    return links

def random_link() -> str:
    links = load_links()
    return random.choice(links)

def extract_url(text: str) -> list[str]:
    if not text: return None
    try:
        return URL_PATTERN.findall(text)[0]
    except Exception:
        return None