"""Funpinpin get current store and partner."""

from funpinpin_cli.core.util.simple_db import db


class Whoami(object):
    """""Get current store and partner interface."""

    def run(self):
        """Run function."""
        shop = db.get("shop")
        partner_name = db.get("partner_name")
        return shop, partner_name
