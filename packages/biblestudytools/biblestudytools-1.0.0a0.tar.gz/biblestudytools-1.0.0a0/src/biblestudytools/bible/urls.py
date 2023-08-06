__all__ = ["construct_book_url", "construct_chapter_url", "get_book_size"]

from re import compile

from bs4 import BeautifulSoup, ResultSet

from .exceptions import check_bible_version_and_book_slug, ChapterNumDoesNotExist
from ..nav import get_markup

_home = "https://www.biblestudytools.com"
_bible = _home + "/{version_code}"
_book = _bible + "/{book_slug}"
_chapter = _book + "/{chapter_num}.html"


def construct_book_url(bible_version: str, book_slug: str) -> str:

    bible_version_code: str

    bible_version_code = check_bible_version_and_book_slug(bible_version, book_slug)
    return _book.format(version_code=bible_version_code, book_slug=book_slug)


def get_book_size(bible_version: str, book_slug: str) -> int:

    url: str
    html: BeautifulSoup
    links: ResultSet

    url = construct_book_url(bible_version, book_slug)
    html = get_markup(url)
    links = html.find_all(href=compile(url + r"/\d+\.html"))

    return len(links)


def construct_chapter_url(bible_version: str, book_slug: str, chapter_num: int) -> str:

    bible_version_code: str
    nb_chapters: int

    bible_version_code = check_bible_version_and_book_slug(bible_version, book_slug)
    nb_chapters = get_book_size(bible_version, book_slug)

    if chapter_num > nb_chapters:
        raise ChapterNumDoesNotExist

    return _chapter.format(version_code=bible_version_code, book_slug=book_slug, chapter_num=chapter_num)
