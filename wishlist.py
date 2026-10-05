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
    username: str,
    wish: str
) -> bool:
    username = username.lstrip("@")
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

def get_user_wishes(username: str) -> list[dict]:
    username = username.lstrip("@")
    wishlist = load_wishlist()
    return [
        item
        for item in wishlist
        if item["username"] == username
    ]

def delete_wish(username: str, wish_number: int) -> bool:
    username = username.lstrip("@")
    wishlist = load_wishlist()
    user_wishes = [
        item
        for item in wishlist
        if item["username"] == username
    ]
    if wish_number < 1 or wish_number > len(user_wishes): return False
    wish_to_delete =  user_wishes[wish_number - 1]
    wishlist.remove(wish_to_delete)
    save_wishlist(wishlist)
    return True