import sys

import click

from catenabible import __version__
from . import nav
from . import exceptions


def print_version(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"""
    catenabible, version {__version__}

    Datasource: https://catenabible.com
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
def catenabible():
    """Print Bible commentaries from https://catenabible.com."""
    pass


@catenabible.command()
@click.argument("book", type=click.STRING)
@click.argument("chapter", type=click.INT)
@click.argument("verse", type=click.INT)
def seek(book: str, chapter: int, verse: int) -> None:
    """
        Display commentaries (catenabible seek -h, for more info).

        Examples: John 3 16, Proverbs 3 5
    """

    try:
        commentaries = nav.get_commentaries_for(book, chapter, verse)
        commentary_texts = [commentary.get_pretty_text for commentary in commentaries]
        click.echo("\n\n".join(commentary_texts))
    except exceptions.BookDoesNotExistError:
        sys.exit("The book you referenced does not exist.")
    except exceptions.NoCommentariesFoundError:
        sys.exit("No commentaries found. Try exploring the next or previous verse.")


if __name__ == "__main__":

    catenabible()
    sys.exit(0)
