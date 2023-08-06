import string
import typing

import bs4
import requests

from . import urls
from . import utils
from . import exceptions


def get_commentary_ids(book_code: utils.BookCode, chapter: int, verse: int) -> typing.List[str]:

    url: str
    request: requests.Response
    html: bs4.BeautifulSoup
    ids: typing.List[str] = []

    url = urls.construct_verse_url(book_code, chapter, verse)
    request = requests.get(url)
    request.encoding = "utf-8"
    html = bs4.BeautifulSoup(request.text, "html.parser")
    divs = html.find_all("div", class_="slideFooter")

    if not divs:
        raise exceptions.NoCommentariesFoundError

    for div in divs:
        ids.append(div.a["href"].split("/")[-1])

    return ids


def get_commentary(_id: str) -> utils.Commentary:

    url: str
    request: requests.Response
    html: bs4.BeautifulSoup
    img: bs4.Tag
    img_url: str
    author: str
    date: str
    text: str
    reading_time: str

    url = urls.construct_commentary_url(_id)
    request = requests.get(url)
    request.encoding = "utf-8"
    html = bs4.BeautifulSoup(request.text, "html.parser")
    div = html.find("div", class_="slideContent")

    img_url = div.img.attrs["src"]
    author = div.h4.text.strip()
    date = div.h5.text.strip()
    text = div.section.text.strip()
    reading_time = div.find("span", class_="footerText").text.strip()

    return utils.Commentary(author, date, text, img_url, reading_time)


def get_commentaries_for(book: str, chapter: int, verse: int) -> typing.List[utils.Commentary]:

    commentaries: typing.List[utils.Commentary]
    book_slug: str = utils.slugify(book)

    if book_slug.startswith(tuple([digit for digit in string.digits])):
        if book_slug[1] == "_":
            book_slug = book_slug[2:] + book_slug[0]
        else:
            book_slug = book_slug[1:] + book_slug[0]

    if book_slug in utils.book_slugs:
        if book_slug in utils.SeptuagintBookCode.__members__.keys():
            commentary_ids = get_commentary_ids(utils.SeptuagintBookCode[book_slug], chapter, verse)
        else:
            commentary_ids = get_commentary_ids(utils.NewTestamentBookCode[book_slug], chapter, verse)
        commentaries = [get_commentary(_id) for _id in commentary_ids]
    else:
        raise exceptions.BookDoesNotExistError

    return commentaries
