"""Funpinpin cli login."""
import re
import requests
from urllib.parse import urlparse
import logging

from funpinpin_cli.config import (
    DEFAULT_SHOP, REDIRECT_URI, PARTNER_API_URL, DOMAIN_SUFFIX
)
from funpinpin_cli.core.util.simple_db import db

from .auth import authenticate
from .util.exception import InvalidStore, StoreNotFound

requests.adapters.DEFAULT_RETRIES = 5


class Login(object):
    """Login interface."""

    PROTOCOL_REGEX = r"^https?\:\/\/"
    PERMANENT_DOMAIN_SUFFIX = r"\.v3\.myfunpinpin\.{}$".format(DOMAIN_SUFFIX)

    def __init__(self, shop=None):
        """Init."""
        self.shop = shop if shop else DEFAULT_SHOP

    def check_url(self, url):
        """Check if domain is valid."""
        admin_url = url + "/admin/"
        resp = requests.head(admin_url)
        if resp.status_code in [200, 303]:
            return url
        elif resp.status_code == 302:
            loc = resp["location"]
            if re.match(Login.PERMANENT_DOMAIN_SUFFIX, loc):
                return loc
        else:
            raise InvalidStore(self.shop)

    def shop_to_permanent_domain(self, shop):
        """Convert shop to permanent domain."""
        url = ""
        if re.match(Login.PROTOCOL_REGEX, shop):
            url = shop
        elif shop.find(".v3.") >= 0:
            url = f"https://{shop}"
        else:
            # product environment, use .com domain
            url = f"https://{shop}.myfunpinpin.{DOMAIN_SUFFIX}"
        # Make a request to see if it exists or
        # if we get redirected to the permanent domain one
        url = self.check_url(url)
        _parsed_url = urlparse(url)
        return _parsed_url.netloc

    def validate_shop(self, shop):
        """Validate shop."""
        url = self.shop_to_permanent_domain(shop)
        if not url:
            raise InvalidStore(self.shop)
        return url

    def login_partner(self, code):
        """Login partner."""
        url = f"{PARTNER_API_URL}/account/callback"
        params = {
            "code": code,
            "redirect_uri": REDIRECT_URI
        }
        resp = requests.get(
            url, params=params, allow_redirects=False
        )
        if resp.status_code > 400:
            raise ValueError("login partner failed.")
        return resp.cookies['p_token']

    def get_user_info(self, p_token):
        """Get user info by p_token."""
        cookies = {"p_token": p_token}
        url = f"{PARTNER_API_URL}/account/user/info"
        sess = requests.session()
        sess.keep_alive = False
        resp = sess.get(url, cookies=cookies)
        if resp.status_code == 200:
            return resp.json()
        raise ValueError("get partner info failed.")

    def get_sandbox_shop(self, p_token):
        """Get sandbox shop from partner."""
        cookies = {"p_token": p_token}
        url = f"{PARTNER_API_URL}/shops/list"
        params = {
            "limit": 999
        }
        resp = requests.get(url, params=params, cookies=cookies)
        if resp.status_code != 200:
            return []
        rv = resp.json()
        if rv.get("total", 0) <= 0:
            return []
        s_shops = [
            item.get("domain", "") for item in rv.get("data", [])
        ]
        return s_shops

    def login_shop(self, partner_id, shop, p_token):
        """Login shop."""
        cookies = {"p_token": p_token}
        url = f"{PARTNER_API_URL}/shops/oauth"
        redirect_uri = f"https://{shop}"
        params = {
            "partner_id": partner_id,
            "redirect_uri": redirect_uri
        }
        logging.info(url, params, cookies)
        resp = requests.get(url, params=params, cookies=cookies)
        if resp.status_code == 200:
            rv = resp.json()
            if "code" in rv and rv["code"] == 10020:
                raise InvalidStore(rv["msg"])
            return rv["authorization_code"]
        raise ValueError("login shop failed.")

    def run(self):
        """Run function."""
        # extract an: save domain
        domain = ""
        if self.shop:
            domain = self.validate_shop(self.shop)

        # authenticate, get partner token
        print("Initiating authentication")
        p_token = db.get("p_token")
        if not p_token:
            # auth account
            account_info = authenticate()

            # login partner, get p_token
            code = account_info.get("code")
            p_token = self.login_partner(code)
            db.set("p_token", p_token)

        # get partner info
        print("Loading available partner organizations")
        partner_info = self.get_user_info(p_token)
        partner_id = partner_info["partner_info"]["partner_id"]
        partner_name = partner_info["partner_info"]["partner_name"]
        db.set("partner_id", partner_id)
        db.set("partner_name", partner_name)

        if not self.shop:
            return domain, partner_name

        # login shop
        sandbox_shopps = self.get_sandbox_shop(p_token)
        if domain not in sandbox_shopps:
            raise InvalidStore(self.shop)

        shop_token = self.login_shop(partner_id, domain, p_token)
        db.set("shop", domain)
        db.set("shop_token", shop_token)
        return domain, partner_name


if __name__ == "__main__":
    login = Login()
    login.run()
