from telethon.sync import TelegramClient, events
from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    CHAT_ID,
    BOT_COMMAND,
    BOT_RANDOM_PLACE_TEXT,
    BOT_SESSION_NAME,
    PLACES_PATH,
    BOT_REMOVE_COMMAND
)
import json
import random
from pathlib import Path
import re
from telethon.tl.types import UpdateMessageReactions

PLACES_DATA = Path(PLACES_PATH)
client = TelegramClient(BOT_SESSION_NAME, API_ID, API_HASH)

URL_PATTERN = re.compile(
    r"https?://2gis.kz[^\s<>\]\)]+",
    re.IGNORECASE,
)

async def main():
    await client.start(
        bot_token=BOT_TOKEN,
    )
    await client.run_until_disconnected()

async def random_place(event, sender):
    place = random_link()
    await event.respond(BOT_RANDOM_PLACE_TEXT.format(
        first_name = sender.first_name,
        place_link = place
    ))

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

def store_places(links: list[str]):
    with PLACES_DATA.open("w", encoding="utf-8") as file:
        json.dump(links, file, ensure_ascii=False, indent=4)

def add_place(text: str):
    links = load_links()
    link = extract_url(text)
    if link is None: return
    if link in links: return
    links.append(link)
    store_places(links)

def remove_place(text: str):
    links = load_links()
    link = extract_url(text)
    if link is None: return
    if link not in links: return
    links.remove(link)
    store_places(links)


@client.on(events.NewMessage(chats=CHAT_ID))
async def debug_handler(event):
    if event.raw_text[:2] == BOT_REMOVE_COMMAND:
        link = event.raw_text[2:].strip()
        print(link)
        remove_place(link)
        return
    add_place(event.raw_text)
    if event.message.reply_to: return
    sender = await event.get_sender()
    if event.raw_text == BOT_COMMAND:
        await random_place(event,sender)
        return

if __name__ == "__main__":
    client.loop.run_until_complete(
        main()
    )