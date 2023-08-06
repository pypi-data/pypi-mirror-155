"""Funpinpin get current store."""

from funpinpin_cli.core.util.simple_db import db


class Store(object):
    """""Get current store interface."""

    def run(self):
        """Run function."""
        shop = db.get("shop")
        return shop
