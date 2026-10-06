from telethon import Button
from pathlib import Path
from config.app import(
    MENU_CONFIG_PATH
)
import json

MENU_CONFIG_DATA = Path(MENU_CONFIG_PATH)

def load_menu_config():
    with MENU_CONFIG_DATA.open("r", encoding = "utf-8") as file:
        menu_config = json.load(file)
    return menu_config

def button_menu():
    menu_config = load_menu_config()
    return [
        Button.inline(title, command)
        for title, command in menu_config.items()
    ]