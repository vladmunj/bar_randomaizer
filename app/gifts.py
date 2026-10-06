import json
from pathlib import Path
from config.app import (
    GIFTS_PATH
)

GIFTS_FILE = Path(GIFTS_PATH)

def load_gifts() -> list[dict]:
    if not GIFTS_FILE.exists(): return []
    with GIFTS_FILE.open("r", encoding="utf-8") as file:
        gifts = json.load(file)
    return gifts

def save_gifts(gifts: list[dict]) -> None:
    with GIFTS_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            gifts,
            file,
            ensure_ascii=False,
            indent=4
        )

def add_gift(
    username: str,
    gift: str
) -> bool:
    username = username.lstrip("@")
    gifts = load_gifts()
    if any(
        item["username"] == username
        and item["gift"].lower() == gift.lower()
        for item in gifts
    ): return False
    gifts.append({
        "username": username,
        "gift": gift
    })
    save_gifts(gifts)
    return True

def delete_gift(username: str, gift_number: int) -> bool:
    username = username.lstrip("@")
    gifts = load_gifts()
    user_gifts = [
        item
        for item in gifts
        if item["username"] == username
    ]
    if gift_number < 1 or gift_number > len(user_gifts): return False
    gift_to_delete =  user_gifts[gift_number - 1]
    gifts.remove(gift_to_delete)
    save_gifts(gifts)
    return True

def get_user_gifts(username: str) -> list[dict]:
    username = username.lstrip("@")
    gifts = load_gifts()
    return [
        item
        for item in gifts
        if item["username"] == username
    ]

def get_user_gifts_list(username: str) -> str | bool:
    gifts = get_user_gifts(username)
    if len(gifts) == 0: return False
    gifts_list = []
    for index, item in enumerate(gifts, start=1):
        gifts_list.append(f"{index}. {item["gift"]}")
    return "\n".join(gifts_list)