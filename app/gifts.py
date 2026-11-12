"""Gifts are stored in the wishlist app (whishlist.cc) and managed through its HTTP API.

Every Telegram user gets one wishlist titled with their username. The bot keeps only a mapping
username -> (list id, edit token) in a small local SQLite database (GIFTS_DB_PATH).
"""
import asyncio
import re
import sqlite3
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup

from config.app import (
    GIFTS_DB_PATH,
    MOVIE_LINKS_HEADERS,
    WISHLIST_API_URL,
    WISHLIST_PUBLIC_URL,
)

GIFT_URL_PATTERN = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)
TITLE_MAX_LENGTH = 200
URL_MAX_LENGTH = 2048
API_TIMEOUT = aiohttp.ClientTimeout(total=10)
PAGE_TIMEOUT = aiohttp.ClientTimeout(total=6)

# Guards list creation so two quick messages from a new user don't create two lists.
_create_lock = asyncio.Lock()


class WishlistError(Exception):
    """The wishlist API is unreachable or rejected the request."""


# --- local mapping username -> list -------------------------------------------------------------

def _db() -> sqlite3.Connection:
    connection = sqlite3.connect(GIFTS_DB_PATH)
    connection.execute(
        """CREATE TABLE IF NOT EXISTS wishlists (
            username TEXT PRIMARY KEY COLLATE NOCASE,
            list_id TEXT NOT NULL,
            edit_token TEXT NOT NULL
        )"""
    )
    return connection


def _normalize(username: str) -> str:
    return username.lstrip("@").strip()


def get_wishlist(username: str) -> tuple[str, str] | None:
    with _db() as connection:
        row = connection.execute(
            "SELECT list_id, edit_token FROM wishlists WHERE username = ?",
            (_normalize(username),),
        ).fetchone()
    return (row[0], row[1]) if row else None


def save_wishlist(username: str, list_id: str, edit_token: str) -> None:
    with _db() as connection:
        connection.execute(
            "INSERT OR REPLACE INTO wishlists (username, list_id, edit_token) VALUES (?, ?, ?)",
            (_normalize(username), list_id, edit_token),
        )


def forget_wishlist(username: str) -> None:
    with _db() as connection:
        connection.execute("DELETE FROM wishlists WHERE username = ?", (_normalize(username),))


def wishlist_url(list_id: str) -> str:
    return f"{WISHLIST_PUBLIC_URL}/list/{list_id}"


# --- wishlist API -------------------------------------------------------------------------------

async def _request(method: str, path: str, token: str | None = None, json: dict | None = None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        async with aiohttp.ClientSession(timeout=API_TIMEOUT) as session:
            async with session.request(
                method, f"{WISHLIST_API_URL}{path}", json=json, headers=headers
            ) as response:
                if response.status == 404:
                    return None
                if response.status >= 400:
                    raise WishlistError(f"{method} {path}: {response.status} {await response.text()}")
                return await response.json() if response.status != 204 else True
    except (aiohttp.ClientError, asyncio.TimeoutError) as error:
        raise WishlistError(f"{method} {path}: {error}") from error


async def _fetch_list(username: str) -> dict | None:
    """The user's list with items, or None if they have none (or it was deleted on the site)."""
    wishlist = get_wishlist(username)
    if not wishlist:
        return None
    data = await _request("GET", f"/{wishlist[0]}")
    if data is None:
        forget_wishlist(username)
    return data


async def _ensure_list(username: str) -> tuple[str, str]:
    async with _create_lock:
        wishlist = get_wishlist(username)
        if wishlist and await _request("GET", f"/{wishlist[0]}") is not None:
            return wishlist
        created = await _request("POST", "", json={"title": _normalize(username)})
        save_wishlist(username, created["id"], created["editToken"])
        return created["id"], created["editToken"]


async def _page_title(url: str) -> str:
    """The product page's title, falling back to the link's domain."""
    fallback = urlparse(url).hostname or url
    try:
        async with aiohttp.ClientSession(timeout=PAGE_TIMEOUT, headers=MOVIE_LINKS_HEADERS) as session:
            async with session.get(url) as response:
                html = await response.text(errors="ignore")
        soup = BeautifulSoup(html, "html.parser")
        og_title = soup.find("meta", property="og:title")
        title = (og_title.get("content") if og_title else None) or (
            soup.title.string if soup.title else None
        )
    except Exception:
        title = None
    title = " ".join((title or "").split()) or fallback
    return title[:TITLE_MAX_LENGTH]


# --- bot-facing functions -----------------------------------------------------------------------

async def add_gift(username: str, gift: str) -> bool:
    """Adds the link to the user's wishlist. False if it is already there."""
    existing = await _fetch_list(username)
    if existing and any((item["url"] or "").lower() == gift.lower() for item in existing["items"]):
        return False
    list_id, token = await _ensure_list(username)
    title = await _page_title(gift)
    await _request("POST", f"/{list_id}/items", token, {"title": title, "url": gift})
    return True


async def delete_gift(username: str, gift_number: int) -> bool:
    wishlist = await _fetch_list(username)
    if not wishlist or gift_number < 1 or gift_number > len(wishlist["items"]):
        return False
    list_id, token = get_wishlist(username)
    item = wishlist["items"][gift_number - 1]
    return await _request("DELETE", f"/{list_id}/items/{item['id']}", token) is not None


async def get_user_gifts(username: str) -> list[dict]:
    wishlist = await _fetch_list(username)
    return wishlist["items"] if wishlist else []


async def get_user_gifts_list(username: str) -> str | bool:
    wishlist = await _fetch_list(username)
    if not wishlist or not wishlist["items"]:
        return False
    lines = [
        f"{index}. {item['title']}\n{item['url'] or ''}".rstrip()
        for index, item in enumerate(wishlist["items"], start=1)
    ]
    lines.append(f"\n🎁 {wishlist_url(wishlist['id'])}")
    return "\n".join(lines)


def extract_gift_url(message: str) -> str | None:
    if not message: return None
    match = GIFT_URL_PATTERN.search(message)
    if not match: return None
    url = match.group(0).rstrip(".,!?;:)]}")
    return url if len(url) <= URL_MAX_LENGTH else None


async def is_chat_member(client, chat_id: int, username: str) -> bool:
    username = username.lstrip("@").lower()
    try:
        async for participant in client.iter_participants(chat_id):
            participant_username = getattr(participant, "username", None)
            if participant_username and participant_username.lower() == username:
                return True
    except Exception as error:
        print(f"Failed to get chat participants: {error}")
        return False
    return False
