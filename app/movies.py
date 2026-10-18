import aiohttp
from io import BytesIO
from telethon import Button
from app.services.tmdb import get_random_movie
from helpers.dic import text
from config.app import (
    TMDB_SOURCE_TYPE_TV,
    DEFAULT_POSTER_RUS
)

async def load_random_movie(event):
    movie = await get_random_movie()
    if movie is None:
        await event.respond(text("movie_not_found"))
        return
    caption = __prepare_cation(movie)
    buttons = __prepare_buttons()
    poster = await load_poster(movie)
    await event.respond(
        file=poster,
        message=caption,
        buttons=buttons,
        parse_mode="md",
        force_document=False
    )

def __prepare_cation(movie):
    return (
        f"🎬 **{movie['title']}**\n"
        f"{text("source_type_tv") if movie['type'] == TMDB_SOURCE_TYPE_TV else text("source_type_movie")}"
        f" · {movie['year']}\n"
        f"⭐ {text("rating")}: {movie['rating'] or text("no_score")}\n\n"
        f"{movie['overview']}"
    )

def __prepare_buttons():
    return [
        [
            Button.inline(
                f"{text("next_random_movie_button_text")}",
                b"random:movie",
            )
        ]
    ]

async def load_poster(movie):
    if not movie["poster_url"]: return str(DEFAULT_POSTER_RUS)
    async with aiohttp.ClientSession() as session:
        async with session.get(
            movie["poster_url"]
        ) as response:
            response.raise_for_status()
            image_data = await response.read()
        return BytesIO(image_data)