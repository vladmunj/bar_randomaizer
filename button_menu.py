from telethon import Button

def button_menu():
    return [
        [
            Button.inline(
                "📋 Мой wishlist",
                b"wishlist:list"
            )
        ]
    ]