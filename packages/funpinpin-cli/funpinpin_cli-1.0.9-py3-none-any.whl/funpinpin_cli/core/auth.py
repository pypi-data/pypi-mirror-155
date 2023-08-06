"""Authentication."""
import threading
import webbrowser
from urllib.parse import urlencode

from funpinpin_cli.core.util.simple_db import db
from funpinpin_cli.core.util.simple_http_server import get_local_server
from funpinpin_cli.core.util.exception import TimeoutException
from funpinpin_cli.config import (
    CLIENT_ID, ACCOUNT_API_URL, REDIRECT_URI,
    AUTH_TIMEOUT
)
import logging


def authorize_with_browser(redirect_uri, scope="", state=""):
    """Authorize with browser."""
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": redirect_uri,
        #"response_type": "code",
        "scope": scope,
        "state": state
    }
    params = urlencode(params)
    url = f"{ACCOUNT_API_URL}/oauth/authorize?{params}"
    logging.info(url)
    webbrowser.open(url)


def check_identity():
    """Check if partner is loggined."""
    pass


def init_authentication(host, port, redirect_uri, scope):
    """Start a thread to open brower and get access code."""
    logging.info("redirect server start: ...")
    server = get_local_server(host, port)
    with server:
        logging.info(f"serving at {host}:{port}")
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        logging.info("Server loop running in thread:", server_thread.name)

        # open browser and authentication
        authorize_with_browser(redirect_uri, scope=scope)

        # wait to get code
        server_thread.join(AUTH_TIMEOUT)
        server.shutdown()

    code = db.get("code")
    if not code:
        raise TimeoutException("timeout, please reauthenticate")

    # use code only once.
    db.delete("code")
    logging.info(f"get code from thread: {code}")
    return code


def authenticate():
    """Get code, exchange for token, save to db."""
    # 1. get code.
    code = init_authentication(
        "127.0.0.1", 3456, REDIRECT_URI,
        "read_product write_product read_order write_order read_shop write_shop"
    )
    return {"code": code}


if __name__ == "__main__":
    authenticate()
