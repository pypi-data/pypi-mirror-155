__all__ = [
    "BibleVersionDoesNotExistError",
    "BookDoesNotExistError",
    "ChapterNumDoesNotExist",
    "VerseDoesNotExistError",
    "check_bible_version_and_book_slug",
]

from biblestudytools.bible.util import bible_versions, bible_version_codes, version_books


class BibleVersionDoesNotExistError(Exception):
    pass


class BookDoesNotExistError(Exception):
    pass


class ChapterNumDoesNotExist(Exception):
    pass


class VerseDoesNotExistError(Exception):
    pass


def check_bible_version_and_book_slug(bible_version: str, book_slug: str) -> str:

    bible_version_code: str
    this_version_books: dict

    if bible_version not in bible_versions.keys():
        raise BibleVersionDoesNotExistError

    try:
        bible_version_code = bible_version_codes[bible_version]
        this_version_books = version_books[bible_version]

        if book_slug not in this_version_books:
            raise BookDoesNotExistError

    except ValueError:
        print("An existing Bible version has no code or assigned books.")
        exit(1)
    else:
        return bible_version_code
