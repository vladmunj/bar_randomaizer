import json
from pathlib import Path
from config import (
    WISHLIST_PATH
)

WISHLIST_FILE = Path(WISHLIST_PATH)

def load_wishlist() -> list[dict]:
    if not WISHLIST_FILE.exists(): return []
    with WISHLIST_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError("wishlist.json должен содержать массив")
    return data

def save_wishlist(wishlist: list[dict]) -> None:
    WISHLIST_FILE.parent.mkdir(parents=True, exist_ok=True)
    with WISHLIST_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            wishlist,
            file,
            ensure_ascii=False,
            indent=4
        )

def add_wish(
    username: str | None,
    wish: str
) -> bool:
    wishlist = load_wishlist()
    if any(
        item["username"] == username
        and item["wish"].lower() == wish.lower()
        for item in wishlist
    ): return False
    wishlist.append({
        "username": username,
        "wish": wish
    })
    save_wishlist(wishlist)
    return True