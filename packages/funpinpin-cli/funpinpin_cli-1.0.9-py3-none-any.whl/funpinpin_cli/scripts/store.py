import click

from funpinpin_cli.core.store import Store

from .message import MSG_NO_STORE


@click.command("store")
def store():
    """
    \b
    \033[96mstore\033[0m: Display current store.
      Usage: \033[96mshopify store\033[0m
    """
    store = Store()
    shop = store.run()
    if not shop:
        msg = MSG_NO_STORE
    else:
        msg = \
            "You're currently logged into " + \
            click.style(f"{shop}", fg="green")

    click.echo(msg)
