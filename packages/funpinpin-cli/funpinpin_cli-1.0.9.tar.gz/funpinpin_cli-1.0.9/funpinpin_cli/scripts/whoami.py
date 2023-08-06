import click

from funpinpin_cli.core.whoami import Whoami

from .message import (
    MSG_NO_PARTNER, get_login_msg
)


@click.command("whoami")
def whoami():
    """
    \b
    \033[96mwhoami\033[0m: Identifies which partner organization or store you are currently logged into.
      Usage: \033[96mshopify whoami\033[0m
    """
    whoami = Whoami()
    shop, partner_name = whoami.run()
    if not shop:
        msg = MSG_NO_PARTNER
    else:
        msg = get_login_msg(shop, partner_name)
    click.echo(msg)
