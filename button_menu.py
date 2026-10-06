from telethon import Button

def button_menu():
    return [
        [
            Button.inline(
                "📋 Мои подарки",
                b"wishlist:list"
            )
        ]
    ]