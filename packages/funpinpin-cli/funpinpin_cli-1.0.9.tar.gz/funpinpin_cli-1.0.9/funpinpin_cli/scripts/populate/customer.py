"""Populate customers command."""
import click

from funpinpin_cli.core.populate import Customer

from ..message import (
    get_populate_begin_msg, get_populate_msg, get_populate_end_msg
)
from .validator import get_prompt, verify_login


@click.command("customers")
@click.option(
    "--count",
    default=5,
    type=click.IntRange(1, 200),
    callback=verify_login,
    help='number of customers.'
)
@click.option('--silent', is_flag=True)
@click.option('--async_run', is_flag=True)
@click.confirmation_option(prompt=get_prompt())
def customers(count, silent, async_run):
    """
    \b
    \033[96mcustomers [options]\033[0m: Add dummy customers to the specified store.
      Usage: \033funpinpin populate customers\033[0m
    """
    try:
        customer = Customer(count)
        click.echo(get_populate_begin_msg(customer.shop))
        if async_run:
            customer_generator = customer.async_run()
        else:
            customer_generator = customer.run()
    except Exception as e:
        click.echo(e)

    if silent:
        succ_count = echo_with_progess_bar(customer_generator, count)
    else:
        succ_count = echo_item(customer_generator, count, customer.shop)

    click.echo(
        get_populate_end_msg(customer.shop, "customers", succ_count)
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
                shop,
                "customers",
                " ".join([obj["firstName"], obj["lastName"]]),
                obj["id"]
            )
            click.echo(msg)
        else:
            click.echo(obj)
    return succ_count
