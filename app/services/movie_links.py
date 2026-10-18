import asyncio
import re
from urllib.parse import quote, urljoin
import aiohttp
from bs4 import BeautifulSoup
from config.app import (
    KINOGO_SEARCH_URL,
    KINOPOISK_SEARCH_URL,
    MOVIE_LINKS_HEADERS,
    KINOGO_BASE_URL,
    KINOPOISK_BASE_URL
)
from helpers.dic import text


def normalize_title(title: str) -> str:
    title = title.casefold().strip()
    title = re.sub(r"\s*\(\d{4}\)\s*", " ", title)
    title = re.sub(r"[^\w\s]", " ", title)
    return " ".join(title.split())

def fetch_first_result(
    html: str,
    site: str,
    expected_title: str,
    expected_year: str | None,
) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    if site == "kinogo":
        result = soup.select_one("article.shortStory")
        if not result: return None
        link = result.select_one(".shortstoryHeader h2 a")
        if not link: return None
        actual_title = link.get("title") or link.get_text(" ", strip=True)
        href = link.get("href")
        year_match = re.search(r"\((\d{4})\)", actual_title)
        actual_year = year_match.group(1) if year_match else None
    elif site == "kinopoisk":
        result = soup.select_one('[data-test-id="movie-list-item"]')
        if not result: return None
        title_element = result.select_one(
            '[data-test-id="next-link"] '
            ".desktop-list-main-info_mainTitle__KPKFM span"
        )
        link = result.select_one('[data-test-id="next-link"]')
        if not title_element or not link: return None
        actual_title = title_element.get_text(" ", strip=True)
        href = link.get("href")
        secondary = result.select_one(
            ".desktop-list-main-info_secondaryText__NeoZN"
        )
        year_match = (
            re.search(r"\b(19\d{2}|20\d{2})\b", secondary.get_text())
            if secondary
            else None
        )
        actual_year = year_match.group(1) if year_match else None
    else:
        return None
    if not href: return None
    if normalize_title(actual_title) != normalize_title(expected_title):
        return None
    if expected_year and actual_year and actual_year != expected_year:
        return None
    base_url = (
        KINOGO_BASE_URL
        if site == "kinogo"
        else KINOPOISK_BASE_URL
    )
    return urljoin(base_url, href)

async def fetch_html(
    session: aiohttp.ClientSession,
    url: str,
) -> str | None:
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()

    except (aiohttp.ClientError, TimeoutError) as error:
        print(f"{text("request_error")} {url}: {error}")
        return None

async def find_movie_links(
    title: str,
    year: str | None = None,
) -> dict[str, str | None]:
    encoded_title = quote(title)
    urls = {
        "kinogo": f"{KINOGO_SEARCH_URL}{encoded_title}",
        "kinopoisk": f"{KINOPOISK_SEARCH_URL}{encoded_title}",
    }
    timeout = aiohttp.ClientTimeout(total=15)
    async with aiohttp.ClientSession(
        headers=MOVIE_LINKS_HEADERS,
        timeout=timeout,
    ) as session:
        kinogo_html, kinopoisk_html = await asyncio.gather(
            fetch_html(session, urls["kinogo"]),
            fetch_html(session, urls["kinopoisk"]),
        )
    return {
        "kinogo_url": (
            fetch_first_result(kinogo_html, "kinogo", title, year)
            if kinogo_html
            else None
        ),
        "kinopoisk_url": (
            fetch_first_result(kinopoisk_html, "kinopoisk", title, year)
            if kinopoisk_html
            else None
        ),
    }