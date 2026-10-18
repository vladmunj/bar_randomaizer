import random
import aiohttp
from config.app import (
    TMDB_API_KEY,
    TMDB_BASE_URL,
    TMDB_IMAGE_URL,
    APP_LOCALE,
    TMDB_MOVIE_TYPES,
    TMDB_MIN_RATING
)
from helpers.dic import text

async def get_random_movie(
    language: str = APP_LOCALE,
    min_rating: float = TMDB_MIN_RATING,
) -> dict | None:
    if not TMDB_API_KEY: raise RuntimeError(text("tmdb_key_not_set"))
    media_type = random.choice(TMDB_MOVIE_TYPES)
    params = {
        "api_key": TMDB_API_KEY,
        "language": language,
        "page": random.randint(1, 10),
        "sort_by": "popularity.desc",
        "vote_average.gte": min_rating,
        "vote_count.gte": 50,
        "include_adult": "false",
    }
    url = f"{TMDB_BASE_URL}/discover/{media_type}"
    timeout = aiohttp.ClientTimeout(total=15)
    async with aiohttp.ClientSession(
        timeout=timeout
    ) as session:
        async with session.get(
            url,
            params=params,
        ) as response:
            response.raise_for_status()
            data = await response.json()
        results = data.get("results", [])
        if not results: return None
        item = random.choice(results)
        title = item.get("name") or item.get("title")
        release_date = item.get("first_air_date") or item.get("release_date")
        poster_path = item.get("poster_path")
        return {
            "id": item["id"],
            "type": media_type,
            "title": title or text("no_title"),
            "overview": item.get("overview") or text("no_description"),
            "rating": item.get("vote_average"),
            "year": (
                release_date[:4]
                if release_date
                else text("unknown")
            ),
            "poster_url": (
                f"{TMDB_IMAGE_URL}{poster_path}"
                if poster_path
                else None
            ),
        }