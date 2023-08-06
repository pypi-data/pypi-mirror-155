import sys

import click

from biblestudytools.bible import get_verses, get_verse
from . import __version__


def print_version(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"""
    biblestudytools, version {__version__}

    Datasource: https://www.biblestudytools.com
    Developer: numbergazing
    Email: hello@numbergazing.com
    """)
    ctx.exit()


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.option(
    "-v", "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Output version information and exit"
)
def main():
    """Print Bible verses from https://www.biblestudytools.com."""
    pass


@main.command()
@click.argument("bible_version", type=click.STRING)
@click.argument("book", type=click.STRING)
@click.argument("chapter", type=click.INT)
@click.argument("vrefs", type=click.STRING)
def seek(bible_version: str, book: str, chapter: int, vrefs: str) -> None:
    """
        Display verses (biblestudytools seek -h, for more info).

        Examples: Septuagint John 3 16, "King James" Genesis 1 1-5
    """

    verses_num = [int(num) for num in vrefs.split("-")]
    bible_version_slug = bible_version.replace(" ", "-").lower()
    book_slug = book.replace(" ", "-").lower()

    if len(verses_num) > 1:
        verses = get_verses(bible_version_slug, book_slug, chapter, first=verses_num[0], last=verses_num[1])
    else:
        verses = [get_verse(bible_version_slug, book_slug, chapter, verses_num[0])]

    verse_strings = [f"     {verse.verse_num}. {verse.text}" for verse in verses]
    click.echo(f"\n     [{bible_version}, {book} {chapter}:{vrefs}]\n")
    click.echo("\n".join(verse_strings))
    click.echo()


if __name__ == "__main__":

    main()
    sys.exit(0)
