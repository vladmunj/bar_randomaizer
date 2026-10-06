import json
from config.app import PLACES_PATH
from app.links import(
    load_links,
    extract_url
)
from pathlib import Path
PLACES_DATA = Path(PLACES_PATH)

def store_places(links: list[dict]):
    with PLACES_DATA.open("w", encoding="utf-8") as file:
        json.dump(links, file, ensure_ascii=False, indent=4)

def is_place_exists(link: str):
    places = load_links()
    return any(
        place["link"] == link
        for place in places
    )

def get_place_link(link: str) -> dict | None:
    places = load_links()
    return next(
        (
            place
            for place in places
            if place.get("link") == link
        ),
        None
    )

def add_place(event):
    link = extract_url(event.raw_text)
    if link is None or is_place_exists(link): return
    places = load_links()
    places.append({
        "chat_id": event.chat.id,
        "message_id": event.message.id,
        "link": link
    })
    store_places(places)

async def remove_place(client, text: str) -> bool:
    link = extract_url(text)
    if link is None: return False
    place = get_place_link(link)
    if not place: return False
    chat_id = place.get("chat_id")
    message_id = place.get("message_id")
    try:
        await client.delete_messages(
            chat_id,
            message_id
        )
    except Exception:
        return False
    places = load_links()
    places = [
        place
        for place in places
        if not (
            place.get("chat_id") == chat_id
            and place.get("message_id") == message_id
        )
    ]
    store_places(places)
    return True