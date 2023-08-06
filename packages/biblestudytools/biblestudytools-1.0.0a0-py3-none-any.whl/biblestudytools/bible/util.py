__all__ = [
    "bible_versions",
    "bible_version_codes",
    "septuagint_books",
    "old_testament_books",
    "new_testament_books",
    "version_books",
    "Verse",
    "chain_replace"
]

from dataclasses import dataclass

bible_versions = {
    "septuagint": "Septuagint",
    "king-james": "King James",
}
bible_version_codes = {
    "septuagint": "lxx",
    "king-james": "kjv",
}
septuagint_books = {
    "genesis": "Genesis",
    "exodus": "Exodus",
    "leviticus": "Leviticus",
    "numbers": "Numbers",
    "deuteronomy": "Deuteronomy",
    "joshua": "Joshua",
    "judges": "Judges",
    "ruth": "Ruth",
    "kings-i": "Kings I",
    "kings-ii": "Kings II",
    "kings-iii": "Kings III",
    "kings-iv": "Kings IV",
    "chronicles-i": "Chronicles I",
    "chronicles-ii": "Chronicles II",
    "ezra": "Ezra",
    "nehemiah": "Nehemiah",
    "esther": "Esther",
    "job": "Job",
    "proverbs": "Proverbs",
    "ecclesiastes": "Ecclesiastes",
    "song-of-songs": "Song of Songs",
    "esias": "Esias",
    "jeremias": "Jeremias",
    "lamentations": "Lamentations",
    "jezekiel": "Jezekiel",
    "daniel": "Daniel",
    "osee": "Osee",
    "joel": "Joel",
    "amos": "Amos",
    "obdias": "Obdias",
    "jonas": "Jonas",
    "michaeas": "Michaeas",
    "nauam": "Naum",
    "ambacum": "Ambacum",
    "sophonias": "Sophonias",
    "aggaeus": "Aggaeus",
    "zacharias": "Zacharias",
    "malachias": "Malachias",
    "tobit": "Tobit",
    "judith": "Judith",
    "wisdom": "Wisdom",
    "sirach": "Sirach",
    "baruch": "Baruch",
    "epistle-of-jeremy": "Epistle of Jeremy",
    "prayer-of-azarias": "Prayer of Azarias",
    "susanna": "Susanna",
    "bel-and-the-dragon": "Bel and the Dragon",
    "i-maccabees": "I Maccabees",
    "ii-maccabees": "II Maccabees",
    "i-esdras": "I Esdras",
    "prayer-of-manasses": "Prayer of Manasses",
    "iii-maccabees": "III Maccabees",
    "iv-maccabees": "IV Maccabees",
}
old_testament_books = {
    "genesis": "Genesis",
    "exodus": "Exodus",
    "leviticus": "Leviticus",
    "numbers": "Numbers",
    "deuteronomy": "Deuteronomy",
    "joshua": "Joshua",
    "judges": "Judges",
    "ruth": "Ruth",
    "1-samuel": "1 Samuel",
    "2-samuel": "2 Samuel",
    "1-kings": "1 Kings",
    "2-kings": "2 Kings",
    "1-chronicles": "1 Chronicles",
    "2-chronicles": "2 Chronicles",
    "ezra": "Ezra",
    "nehemiah": "Nehemiah",
    "esther": "Esther",
    "job": "Job",
    "psalms": "Psalms",
    "proverbs": "Proverbs",
    "ecclesiastes": "Ecclesiastes",
    "song-of-solomon": "Song of Solomon",
    "isaiah": "Isaiah",
    "jeremiah": "Jeremiah",
    "lamentations": "Lamentations",
    "ezekiel": "Ezekiel",
    "daniel": "Daniel",
    "hosea": "Hosea",
    "joel": "Joel",
    "amos": "Amos",
    "obadiah": "Obadiah",
    "jonah": "Jonah",
    "micah": "Micah",
    "nahum": "Nahum",
    "habakukk": "Habakukk",
    "zephaniah": "Zephaniah",
    "haggai": "Haggai",
    "zechariah": "Zechariah",
    "malachias": "Malachias",
    "malachi": "Malachi",
}
new_testament_books = {
    "matthew": "Matthew",
    "mark": "Mark",
    "luke": "Luke",
    "john": "John",
    "acts": "Acts",
    "romans": "Romans",
    "1-corinthians": "1 Corinthians",
    "2-corinthians": "2 Corinthians",
    "galatians": "Galatians",
    "ephesians": "Ephesians",
    "philippians": "Philippians",
    "colossians": "Colossians",
    "1-thessalonians": "1 Thessalonians",
    "2-thessalonians": "2 Thessalonians",
    "1-timothy": "1 Timothy",
    "2-timothy": "2 Timothy",
    "titus": "Titus",
    "philemon": "Philemon",
    "hebrews": "Hebrews",
    "james": "James",
    "1-peter": "1 Peter",
    "2-peter": "2 Peter",
    "1-john": "1 john",
    "2-john": "2 john",
    "3-john": "3 john",
    "jude": "Jude",
    "revelation": "Revelation",
}
version_books = {
    "septuagint": septuagint_books,
    "king-james": old_testament_books | new_testament_books
}


@dataclass
class Verse:

    bible_version: str
    book: str
    chapter_num: int
    verse_num: int
    text: str


def chain_replace(string: str, old: list[str], new: str) -> str:
    for word in old:
        string = string.replace(word, new)
    return string
