from config import BOT_RANDOM_PLACE_TEXT
from app.links import random_link

async def random_place(event, sender):
    await event.respond(BOT_RANDOM_PLACE_TEXT.format(
        first_name = sender.first_name,
        place_link = random_link()
    ))