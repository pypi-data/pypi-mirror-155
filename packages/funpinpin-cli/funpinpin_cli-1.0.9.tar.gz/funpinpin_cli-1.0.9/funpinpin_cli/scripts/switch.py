import click

from funpinpin_cli.core.switch import Switch
from funpinpin_cli.core.util.exception import (
    SameStore, InvalidStore, StoreNotFound
)
from .message import (
    get_switch_same_strore_msg, get_invalid_shop_msg,
    MSG_NO_STORE
)


@click.command("switch")
@click.option("--store", help='shop domain')
def switch(store):
    """
    \b
    \033[96mswitch\033[0m: Switch between development stores in your partner organization
      Usage: \033[96mshopify switch [--store STORE]\033[0m
    """
    try:
        switch = Switch(store)
        shop, _ = switch.run()
    except ValueError as e:
        click.echo(e)
        return
    except SameStore:
        click.echo(get_switch_same_strore_msg(switch.shop))
        return
    except InvalidStore:
        click.echo(get_invalid_shop_msg(switch.shop))
        return
    except StoreNotFound:
        click.echo(MSG_NO_STORE)
        return

    msg = \
        "Switched development store to " + \
        click.style(f"{shop} ", fg="green")
    click.echo(msg)
