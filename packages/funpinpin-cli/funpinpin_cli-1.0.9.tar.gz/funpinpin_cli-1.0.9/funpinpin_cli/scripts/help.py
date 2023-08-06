import click

from . import command


@click.command("help")
def help():
    """
    \b
    \033[96mhelp\033[0m: Help command
    """
    click.echo(command.cli.__doc__)
