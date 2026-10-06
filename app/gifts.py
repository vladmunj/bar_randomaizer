# async def gifts(event, sender):
#     text = event.raw_text.strip()
#     if text.startswith(BOT_WISHLIST_ADD_COMMAND):
#         wish = text.replace(BOT_WISHLIST_ADD_COMMAND,"").strip()
#         if not wish:
#             await event.respond(BOT_WISHLIST_EMPTY_TEXT)
#             return
#         added = add_wish(
#             username = sender.username,
#             wish = wish
#         )
#         if not added:
#             await event.respond(BOT_WISHLISH_EXISTS_TEXT)
#             return
#         await event.respond(BOT_WISHLIST_ADDED_TEXT)
#         return
#     if text.startswith(BOT_WISHLIST_LIST_COMMAND):
#         username = text.replace(BOT_WISHLIST_LIST_COMMAND,"").strip() or sender.username
#         await load_user_wishes(username, event)
#         return
#     if text.startswith(BOT_WISHLIST_DELETE_COMMAND):
#         try:
#             wish_num = int(text.replace(BOT_WISHLIST_DELETE_COMMAND,"").strip())
#         except Exception:
#             wish_num = None
#         if not wish_num:
#             wish_count = await load_user_wishes(sender.username, event)
#             if wish_count > 0: await event.respond(BOT_WISHLIST_CHOOSE_WISH_TO_DELETE_TEXT)
#             return
#         wish_deleted = delete_wish(sender.username,wish_num)
#         if not wish_deleted:
#             await event.respond(BOT_WISHLIST_NUM_NOT_FOUND_TEXT)
#             return
#         await event.respond(BOT_WISHLIST_DELETED_SUCCESS_TEXT)
#         return

# async def load_user_wishes(username, event) -> int:
#     try:
#         user = await client.get_entity(username)
#     except Exception:
#         return 0
#     wishes = get_user_wishes(username)
#     if not wishes:
#         await event.respond(BOT_WISHLIST_NOT_FOUND_TEXT.format(
#             wish_add_cmd = BOT_WISHLIST_ADD_COMMAND,
#             first_name = user.first_name
#         ))
#         return 0
#     response = [
#         BOT_WISHLIST_TITLE_TEXT.format(
#             first_name = user.first_name
#         ),
#         ""
#     ]
#     for index, item in enumerate(wishes, start = 1):
#         response.append(f"{index}. {item["wish"]}")
#     await event.respond("\n".join(response))
#     return len(wishes)

# @client.on(events.NewMessage())
# async def debug_handler(event):
#     if event.raw_text[:2] == BOT_REMOVE_COMMAND:
#         link = event.raw_text[2:].strip()
#         print(link)
#         remove_place(link)
#         return
#     add_place(event.raw_text)
#     if event.message.reply_to: return
#     sender = await event.get_sender()
#     if event.raw_text == BOT_COMMAND:
#         await random_place(event,sender)
#         return
#     if event.raw_text.startswith((
#         BOT_WISHLIST_ADD_COMMAND,
#         BOT_WISHLIST_LIST_COMMAND,
#         BOT_WISHLIST_DELETE_COMMAND,
#     )):
#         await wishlist(event,sender)
#         return
#     if event.raw_text == BOT_BUTTON_MENU_COMMAND:
#         await event.respond(
#             BOT_MENU_TITLE_TEXT,
#             buttons = button_menu()
#         )
#         return