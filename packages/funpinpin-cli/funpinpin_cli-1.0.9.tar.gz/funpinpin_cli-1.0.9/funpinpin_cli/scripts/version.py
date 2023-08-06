import click

from funpinpin_cli.core.version import Version


@click.command("version")
def version():
    """
    \b
    \033[96mversion\033[0m: Prints version number.
      Usage: \033[96mfunpinpin version\033[0m
    """
    version = Version()
    version.run()
