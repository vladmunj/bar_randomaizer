import aiohttp
from io import BytesIO
from telethon import Button
from app.services.tmdb import get_random_movie
from helpers.dic import text
from config.app import (
    TMDB_SOURCE_TYPE_TV,
    DEFAULT_POSTER_RUS
)
from pathlib import Path
from urllib.parse import urlparse

class NamedBytesIO(BytesIO):
    def __init__(self, data: bytes, filename: str):
        super().__init__(data)
        self.name = filename

async def load_random_movie(event, edit = False):
    movie = await get_random_movie()
    if movie is None:
        await event.respond(text("movie_not_found"))
        return
    caption = __prepare_caption(movie)
    buttons = __prepare_buttons(movie)
    poster = await load_poster(movie)
    if edit:
        await event.edit(
            file=poster,
            text=caption,
            buttons=buttons,
            parse_mode="md",
            force_document=False
        )
        return
    await event.respond(
        file=poster,
        message=caption,
        buttons=buttons,
        parse_mode="md",
        force_document=False
    )

def __prepare_caption(movie):
    return (
        f"{ "📺" if movie['type'] == TMDB_SOURCE_TYPE_TV else "🎬" } **{movie['title']}**\n"
        f"{text("source_type_tv") if movie['type'] == TMDB_SOURCE_TYPE_TV else text("source_type_movie")}"
        f" · {movie['year']}\n"
        f"⭐ {text("rating")}: {movie['rating'] or text("no_score")}\n\n"
        f"{movie['overview']}"
    )

def __prepare_buttons(movie):
    buttons = []
    if movie.get("trailer_url"):
        buttons.append([
            Button.url(
                f"🎞 {text("source_trailer_title")}",
                movie["trailer_url"],
            )
        ])
    buttons.append([
        Button.inline(
            f"{text("next_random_movie_button_text")}",
            b"random:movie:next",
        )
    ])
    return buttons

async def load_poster(movie):
    timeout = aiohttp.ClientTimeout(total=15)
    if not movie["poster_url"]:
        fallback_path = Path(DEFAULT_POSTER_RUS)
        image_data = fallback_path.read_bytes()
        return NamedBytesIO(image_data, fallback_path.name)
    poster_url = movie.get("poster_url")
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(
            poster_url
        ) as response:
            response.raise_for_status()
            image_data = await response.read()
        filename = Path(urlparse(poster_url).path).name
        if not Path(filename).suffix: filename = "poster.jpg"
        return NamedBytesIO(image_data, filename)