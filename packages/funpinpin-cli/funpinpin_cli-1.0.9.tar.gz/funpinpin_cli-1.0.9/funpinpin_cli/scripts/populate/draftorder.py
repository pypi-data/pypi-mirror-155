"""Populate draftorders command."""
import click

from funpinpin_cli.core.populate import Order

from ..message import (
    get_populate_begin_msg, get_populate_msg, get_populate_end_msg
)
from .validator import get_prompt, verify_login


@click.command("draftorders")
@click.option(
    "--count",
    default=5,
    type=click.IntRange(1, 200),
    callback=verify_login,
    help='number of draftorders.'
)
@click.option('--silent', is_flag=True)
@click.confirmation_option(prompt=get_prompt())
def draftorders(count):
    """
    \b
    \033[96mdraftorders [options]\033[0m: Add dummy orders to the specified store.
      Usage: \033[96mfunpinpin populate draftorders\033[0m
    """
    try:
        order = Order()
        click.echo(get_populate_begin_msg(order.shop))
        order.run()
    except Exception as e:
        click.echo(e)
