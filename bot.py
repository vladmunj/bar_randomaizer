import asyncio
from telethon.sync import TelegramClient, events
from app.places import (
    add_place,
    remove_place
)
from config.app import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    BOT_SESSION_NAME,
    BOT_BUTTON_MENU_COMMAND,
    BOT_BUTTON_MENU_COMMAND_SIMPLE,
    BOT_BUTTON_MENU_COMMAND_START
)
from app.menu import button_menu
from helpers.dic import text
from app.random import random_place
from app.actions import (
    get_action,
    set_action,
    clear_action
)
from app.gifts import (
    add_gift,
    get_user_gifts_list,
    delete_gift,
    extract_gift_url,
    is_chat_member
)
from app.movies import load_random_movie

client = TelegramClient(BOT_SESSION_NAME, API_ID, API_HASH)

from app.message_cleanup import (
    add_message_to_delete,
    delete_messages_from_pool,
)

async def main():
    await client.start(
        bot_token=BOT_TOKEN,
    )
    await client.run_until_disconnected()

@client.on(events.NewMessage())
async def debug_handler(event):
    add_place(event)
    event_text = event.raw_text.strip()
    if event_text in (
            BOT_BUTTON_MENU_COMMAND,
            BOT_BUTTON_MENU_COMMAND_SIMPLE,
            BOT_BUTTON_MENU_COMMAND_START
    ):
        await event.respond(
            text("bot_menu_title"),
            buttons = button_menu()
        )
        return
    user = await event.get_sender()
    action = get_action(user.id)
    match action:
        case "remove_bar":
            clear_action(user.id)
            place_removed = await remove_place(client, event_text)
            if not place_removed:
                await event.respond(text("bar_not_removed"))
                return
            await event.respond(text("bar_removed"))
        case "add_gift":
            clear_action(user.id)
            gift_url = extract_gift_url(event_text)
            if not gift_url:
                await event.respond(text("gift_empty"))
                return
            added_gift = add_gift(user.username, gift_url)
            if not added_gift:
                response = await event.respond(text("gift_exists"))
            else:
                response = await event.respond(text("gift_added"))
            add_message_to_delete(event.chat_id,user.id,event.id)
            add_message_to_delete(event.chat_id,user.id,response.id)
            asyncio.create_task(
                delete_messages_from_pool(
                    client,
                    event.chat_id,
                    user.id,
                    delay=5,
                )
            )
        case "remove_gift":
            clear_action(user.id)
            try:
                gift_num = int(event_text.strip())
            except ValueError:
                await event.respond(text("gift_number_empty"))
                return
            removed_gift = delete_gift(user.username, gift_num)
            if not removed_gift:
                await event.respond(text("gift_number_not_found"))
                return
            await event.respond(text("gift_removed"))
        case "others_gifts":
            clear_action(user.id)
            username = event_text.strip()
            if not username.startswith("@"):
                await event.respond(text("incorrect_username"))
                return
            is_member = await is_chat_member(
                client,
                event.chat_id,
                username
            )
            if not is_member:
                await event.respond(text("unknown_username"))
                return
            gifts_list = get_user_gifts_list(username)
            if not gifts_list:
                await event.respond(text("empty_gifts_list"))
                return
            await event.respond(gifts_list)
        case _:
            return

@client.on(events.CallbackQuery())
async def callback_handler(event):
    await event.answer()
    sender = await event.get_sender()
    command = event.data.decode()
    match command:
        case "bar:random":
            await random_place(event, sender)
        case "bar:remove":
            clear_action(sender.id)
            set_action(sender.id, "remove_bar")
            await event.respond(text("set_bar_link"))
        case "gifts:my":
            gifts_list = get_user_gifts_list(sender.username)
            if not gifts_list:
                await event.respond(text("empty_gifts_list"))
                return
            await event.respond(gifts_list)
        case "gifts:add":
            clear_action(sender.id)
            set_action(sender.id, "add_gift")
            response = await event.respond(text("what_gift"))
            add_message_to_delete(event.chat_id,sender.id,response.id)
        case "gifts:remove":
            clear_action(sender.id)
            set_action(sender.id, "remove_gift")
            gifts_list = get_user_gifts_list(sender.username)
            if not gifts_list:
                await event.respond(text("empty_gifts_list"))
                return
            await event.respond(gifts_list)
            await event.respond(text("what_gift_to_remove"))
        case "gifts:others":
            clear_action(sender.id)
            set_action(sender.id, "others_gifts")
            await event.respond(text("whose_gifts_we_arelooking_for"))
        case "random:movie":
            await load_random_movie(event)
        case "random:movie:next":
            await load_random_movie(event, True)
        case _:
            return

if __name__ == "__main__": asyncio.run(main())