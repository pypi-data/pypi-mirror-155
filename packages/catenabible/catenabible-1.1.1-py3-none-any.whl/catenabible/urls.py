from .utils import BookCode

HOME = "https://catenabible.com"
VERSE_URL = HOME + "/{book_code}/{chapter}/{verse}"
COMMENTARY_URL = HOME + "/com/{id}"


def construct_verse_url(book_code: BookCode, chapter: int, verse: int) -> str:
    return VERSE_URL.format(book_code=book_code.value, chapter=chapter, verse=verse)


def construct_commentary_url(_id: str) -> str:
    return COMMENTARY_URL.format(id=_id)
