import json
from config import PLACES_PATH
from app.random import (
    load_links
)
from app.links import extract_url

PLACES_DATA = Path(PLACES_PATH)

def store_places(links: list[str]):
    with PLACES_DATA.open("w", encoding="utf-8") as file:
        json.dump(links, file, ensure_ascii=False, indent=4)

def add_place(text: str):
    links = load_links()
    link = extract_url(text)
    if link is None or link in links: return
    links.append(link)
    store_places(links)

def remove_place(text: str):
    links = load_links()
    link = extract_url(text)
    if link is None or link not in links: return
    links.remove(link)
    store_places(links)