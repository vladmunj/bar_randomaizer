import aiohttp
from io import BytesIO
from telethon import Button
from app.services.tmdb import get_random_movie
from helpers.dic import text
from config.app import (
    TMDB_SOURCE_TYPE_TV,
    DEFAULT_POSTER_RUS,
    MIME_TYPE_JPEG
)
from pathlib import Path
import mimetypes
from urllib.parse import urlparse

class NamedBytesIO(BytesIO):
    def __init__(self, data: bytes, filename: str):
        super().__init__(data)
        self.name = filename

async def load_random_movie(event):
    movie = await get_random_movie()
    if movie is None:
        await event.respond(text("movie_not_found"))
        return
    caption = __prepare_caption(movie)
    buttons = __prepare_buttons()
    poster, mime_type = await load_poster(movie)
    await event.respond(
        file=poster,
        message=caption,
        buttons=buttons,
        parse_mode="md",
        force_document=False,
        mime_type=mime_type
    )

def __prepare_caption(movie):
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
    timeout = aiohttp.ClientTimeout(total=15)
    if not movie["poster_url"]:
        fallback_path = Path(DEFAULT_POSTER_RUS)
        image_data = fallback_path.read_bytes()
        mime_type = (
            mimetypes.guess_type(fallback_path.name)[0]
            or MIME_TYPE_JPEG
        )
        return NamedBytesIO(image_data, fallback_path.name), mime_type
    poster_url = movie.get("poster_url")
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(
            poster_url
        ) as response:
            response.raise_for_status()
            image_data = await response.read()
        filename = Path(urlparse(poster_url).path).name
        if not Path(filename).suffix: filename = "poster.jpg"
        mime_type = (
            mimetypes.guess_type(filename)[0]
            or MIME_TYPE_JPEG
        )
        return NamedBytesIO(image_data, filename), mime_type