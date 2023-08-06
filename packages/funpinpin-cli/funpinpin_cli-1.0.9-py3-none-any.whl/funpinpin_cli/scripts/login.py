import click

from funpinpin_cli.core.login import Login
from funpinpin_cli.config import DEFAULT_SHOP
from funpinpin_cli.core.util.exception import (
    InvalidStore, StoreNotFound
)

from .message import (
    get_invalid_shop_msg, MSG_NO_STORE,
    get_login_msg
)


@click.command("login")
@click.option("--store", default=DEFAULT_SHOP, help='shop domain')
def login(store):
    """
    \b
    \033[96mlogin\033[0m: Log in to the Funpinpin CLI by authenticating with a store or partner organization
      Usage: \033[96mshopify login [--store STORE]\033[0m
    """
    try:
        login = Login(store)
        shop, partner_name = login.run()
    except InvalidStore as e:
        msg = get_invalid_shop_msg(str(e))
        click.echo(msg)
        return
    except StoreNotFound:
        msg = MSG_NO_STORE
        click.echo(msg)
        return
    except Exception as e:
        click.echo(str(e))
        return
    msg = get_login_msg(shop, partner_name)
    click.echo(msg)
