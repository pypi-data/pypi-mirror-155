"""Populate validator."""

import click

from funpinpin_cli.core.util.simple_db import db

from ..message import MSG_NO_STORE


def get_prompt():
    """Get double check message."""
    shop = db.get("shop")
    prompt = (
        "? You are currently logged into " +
        click.style(f"{shop}", fg="green") +
        ". Do you want to proceed using this store?"
    )
    return prompt


def verify_login(ctx, param, value):
    """Verify if login."""
    shop = db.get("shop")
    if not shop:
        click.echo(MSG_NO_STORE)
        ctx.exit()
    return value
