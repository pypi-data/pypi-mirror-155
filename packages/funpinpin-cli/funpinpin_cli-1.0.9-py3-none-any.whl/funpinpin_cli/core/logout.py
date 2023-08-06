"""Funpinpin cli logout."""

from funpinpin_cli.core.util.simple_db import db


class Logout(object):
    """Logout interface."""

    def run(self):
        """Run function.

        clear stored token.
        """
        try:
            db.delete("p_token")
            db.delete("partner_id")
            db.delete("partner_name")
            db.delete("shop")
            db.delete("shop_token")
        except KeyError:
            pass
