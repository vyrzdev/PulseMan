import click
import unqlite
from . import config
database = unqlite.UnQLite(filename=config.dbLocation)

from . import authenticate


@click.group()
def cli():
    pass


cli.add_command(authenticate.auth)


if __name__ == "__main__":
    cli()
