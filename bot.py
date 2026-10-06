# import json
# import random
# import re
import asyncio
# import os
from telethon.sync import TelegramClient, events
# from pathlib import Path
# from telethon.tl.types import UpdateMessageReactions
from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
#     CHAT_ID,
#     BOT_COMMAND,
#     BOT_RANDOM_PLACE_TEXT,
    BOT_SESSION_NAME,
#     PLACES_PATH,
#     BOT_REMOVE_COMMAND,
#     BOT_WISHLIST_ADD_COMMAND,
#     BOT_WISHLIST_EMPTY_TEXT,
#     BOT_WISHLIST_ADDED_TEXT,
#     BOT_WISHLISH_EXISTS_TEXT,
#     BOT_WISHLIST_LIST_COMMAND,
#     BOT_WISHLIST_TITLE_TEXT,
#     BOT_WISHLIST_NOT_FOUND_TEXT,
#     BOT_WISHLIST_DELETE_COMMAND,
#     BOT_WISHLIST_CHOOSE_WISH_TO_DELETE_TEXT,
#     BOT_WISHLIST_NUM_NOT_FOUND_TEXT,
#     BOT_WISHLIST_DELETED_SUCCESS_TEXT,
#     BOT_BUTTON_MENU_COMMAND,
    BOT_MENU_TITLE_TEXT
)
# from wishlist import(
#     add_wish,
#     get_user_wishes,
#     delete_wish
# )
from app.menu import button_menu

client = TelegramClient(BOT_SESSION_NAME, API_ID, API_HASH)

async def main():
    await client.start(
        bot_token=BOT_TOKEN,
    )
    await client.run_until_disconnected()

@client.on(events.NewMessage())
async def debug_handler(event):
    match event.raw_text:
        case BOT_BUTTON_MENU_COMMAND:
            await event.respond(
                BOT_MENU_TITLE_TEXT,
                buttons = button_menu()
            )
    # if event.raw_text[:2] == BOT_REMOVE_COMMAND:
    #     link = event.raw_text[2:].strip()
    #     print(link)
    #     remove_place(link)
    #     return
    # add_place(event.raw_text)
    # if event.message.reply_to: return
    # sender = await event.get_sender()
    # if event.raw_text == BOT_COMMAND:
    #     await random_place(event,sender)
    #     return
    # if event.raw_text.startswith((
    #     BOT_WISHLIST_ADD_COMMAND,
    #     BOT_WISHLIST_LIST_COMMAND,
    #     BOT_WISHLIST_DELETE_COMMAND,
    # )):
    #     await wishlist(event,sender)
    #     return
    # if event.raw_text == BOT_BUTTON_MENU_COMMAND:
    #     await event.respond(
    #         BOT_MENU_TITLE_TEXT,
    #         buttons = button_menu()
    #     )
    #     return

if __name__ == "__main__": asyncio.run(main())