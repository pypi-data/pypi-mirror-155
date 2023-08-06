from bs4 import BeautifulSoup
from requests import get


def get_markup(url: str, parser: str = "html.parser") -> BeautifulSoup:
    r = get(url)
    r.encoding = "utf-8"
    return BeautifulSoup(r.text, parser)
