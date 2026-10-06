import json
import random
import re
import asyncio
import os
from telethon.sync import TelegramClient, events
from pathlib import Path
from telethon.tl.types import UpdateMessageReactions
from threading import Thread
from flask import Flask
from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    CHAT_ID,
    BOT_COMMAND,
    BOT_RANDOM_PLACE_TEXT,
    BOT_SESSION_NAME,
    PLACES_PATH,
    BOT_REMOVE_COMMAND,
    BOT_WISHLIST_ADD_COMMAND,
    BOT_WISHLIST_EMPTY_TEXT,
    BOT_WISHLIST_ADDED_TEXT,
    BOT_WISHLISH_EXISTS_TEXT,
    BOT_WISHLIST_LIST_COMMAND,
    BOT_WISHLIST_TITLE_TEXT,
    BOT_WISHLIST_NOT_FOUND_TEXT,
    BOT_WISHLIST_DELETE_COMMAND,
    BOT_WISHLIST_CHOOSE_WISH_TO_DELETE_TEXT,
    BOT_WISHLIST_NUM_NOT_FOUND_TEXT,
    BOT_WISHLIST_DELETED_SUCCESS_TEXT,
    BOT_MENU_TITLE_TEXT
)
from wishlist import(
    add_wish,
    get_user_wishes,
    delete_wish
)
from button_menu import button_menu

# ============================================================
# HTTP SERVER
# ============================================================

app = Flask(__name__)
@app.route("/")
def index():
    return "Bot is running", 200

@app.route("/health")
def health():
    return "OK", 200

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False
    )

# ============================================================
# TELEGRAM BOT
# ============================================================

PLACES_DATA = Path(PLACES_PATH)
client = TelegramClient(BOT_SESSION_NAME, API_ID, API_HASH)

URL_PATTERN = re.compile(
    r"https?://2gis.kz[^\s<>\]\)]+",
    re.IGNORECASE,
)

# ============================================================
# START
# ============================================================
async def main():
    print("Starting HTTP server...")
    http_thread = Thread(
        target=run_http_server,
        daemon=True
    )
    http_thread.start()
    print("Starting Telegram bot...")
    await client.start(
        bot_token=BOT_TOKEN,
    )
    print("Telegram bot started")
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

async def wishlist(event, sender):
    text = event.raw_text.strip()
    if text.startswith(BOT_WISHLIST_ADD_COMMAND):
        wish = text.replace(BOT_WISHLIST_ADD_COMMAND,"").strip()
        if not wish:
            await event.respond(BOT_WISHLIST_EMPTY_TEXT)
            return
        added = add_wish(
            username = sender.username,
            wish = wish
        )
        if not added:
            await event.respond(BOT_WISHLISH_EXISTS_TEXT)
            return
        await event.respond(BOT_WISHLIST_ADDED_TEXT)
        return
    if text.startswith(BOT_WISHLIST_LIST_COMMAND):
        username = text.replace(BOT_WISHLIST_LIST_COMMAND,"").strip() or sender.username
        await load_user_wishes(username, event)
        return
    if text.startswith(BOT_WISHLIST_DELETE_COMMAND):
        try:
            wish_num = int(text.replace(BOT_WISHLIST_DELETE_COMMAND,"").strip())
        except Exception:
            wish_num = None
        if not wish_num:
            wish_count = await load_user_wishes(sender.username, event)
            if wish_count > 0: await event.respond(BOT_WISHLIST_CHOOSE_WISH_TO_DELETE_TEXT)
            return
        wish_deleted = delete_wish(sender.username,wish_num)
        if not wish_deleted:
            await event.respond(BOT_WISHLIST_NUM_NOT_FOUND_TEXT)
            return
        await event.respond(BOT_WISHLIST_DELETED_SUCCESS_TEXT)
        return
    if text.startswith(BOT_BUTTON_MENU_COMMAND):
        await event.respond(
            BOT_MENU_TITLE_TEXT,
            buttons = button_menu()
        )
        return

async def load_user_wishes(username, event) -> int:
    try:
        user = await client.get_entity(username)
    except Exception:
        return 0
    wishes = get_user_wishes(username)
    if not wishes:
        await event.respond(BOT_WISHLIST_NOT_FOUND_TEXT.format(
            wish_add_cmd = BOT_WISHLIST_ADD_COMMAND,
            first_name = user.first_name
        ))
        return 0
    response = [
        BOT_WISHLIST_TITLE_TEXT.format(
            first_name = user.first_name
        ),
        ""
    ]
    for index, item in enumerate(wishes, start = 1):
        response.append(f"{index}. {item["wish"]}")
    await event.respond("\n".join(response))
    return len(wishes)

@client.on(events.NewMessage())
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
    if event.raw_text.startswith((
        BOT_WISHLIST_ADD_COMMAND,
        BOT_WISHLIST_LIST_COMMAND,
        BOT_WISHLIST_DELETE_COMMAND,
        BOT_BUTTON_MENU_COMMAND
    )):
        await wishlist(event,sender)
        return

if __name__ == "__main__":
    asyncio.run(main())