"""Funpinpin switch store."""

from funpinpin_cli.core.util.simple_db import db
from funpinpin_cli.core.util.exception import SameStore

from .login import Login


class Switch(Login):
    """Switch store interface."""

    def __init__(self, *args, **kwargs):
        """Init parent class."""
        if not args[0]:
            shop = db.get('shop')
            super(Switch, self).__init__(shop, **kwargs)
        else:
            super(Switch, self).__init__(*args, **kwargs)

    def run(self):
        """Run function, overwrite parent run function."""
        domain = self.validate_shop(self.shop)
        cur_shop = db.get("shop")
        if domain == cur_shop:
            raise SameStore(cur_shop)
        p_token = db.get("p_token")
        if p_token:
            partner_id = db.get("partner_id")
            shop_token = self.login_shop(partner_id, domain, p_token)
            db.set("shop", domain)
            db.set("shop_token", shop_token)
            return domain, ""
        domain, _ = super(Switch, self).run()
        return domain, ""
