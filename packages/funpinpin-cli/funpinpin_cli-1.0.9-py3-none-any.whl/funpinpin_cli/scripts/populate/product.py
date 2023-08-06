"""Populate products command."""
import click

from funpinpin_cli.core.populate import Product

from ..message import (
    get_populate_begin_msg, get_populate_msg, get_populate_end_msg
)
from .validator import get_prompt, verify_login


@click.command("products")
@click.option(
    "--count",
    default=5,
    type=click.IntRange(1, 200),
    callback=verify_login,
    help='number of products.'
)
@click.option('--silent', is_flag=True)
@click.option('--async_run', is_flag=True)
@click.confirmation_option(prompt=get_prompt())
def products(count, silent, async_run):
    """
    \b
    \033[96mproducts [options]\033[0m: Add dummy products to the specified store.
      Usage: \033[96mfunpinpin populate products\033[0m
    """
    try:
        product = Product(count)
        click.echo(get_populate_begin_msg(product.shop))
        if async_run:
            product_generator = product.async_run()
        else:
            product_generator = product.run()
    except Exception as e:
        click.echo(e)

    if silent:
        succ_count = echo_with_progess_bar(product_generator, count)
    else:
        succ_count = echo_item(product_generator, count, product.shop)

    click.echo(
        get_populate_end_msg(product.shop, "products", succ_count)
    )


def echo_with_progess_bar(iterator, count):
    """Echo silently with progress bar."""
    succ_count = 0
    with click.progressbar(iterator, length=count) as bar:
        for status, obj in bar:
            if status:
                succ_count += 1
            else:
                click.echo(obj)
    return succ_count


def echo_item(iterator, count, shop):
    """Echo item detail."""
    succ_count = 0
    for status, obj in iterator:
        if status:
            succ_count += 1
            msg = get_populate_msg(
                shop, "products", obj["title"], obj["id"]
            )
            click.echo(msg)
        else:
            click.echo(obj)
    return succ_count
