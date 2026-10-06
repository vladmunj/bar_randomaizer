from app.links import random_link
from helpers.dic import text

async def random_place(event, sender):
    await event.respond(text("random_place_text").format(
        first_name = sender.first_name,
        place_link = random_link()
    ))