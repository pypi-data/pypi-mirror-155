"""A simple http server."""

import logging
from urllib.parse import urlparse
from urllib.parse import parse_qs
import socketserver
from http.server import SimpleHTTPRequestHandler
from funpinpin_cli.core.util.simple_db import db
from funpinpin_cli.core.util.exception import CodeException
from socketserver import TCPServer, BaseRequestHandler
from typing import Tuple, Callable


RESP_SNIPPET = """<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="shortcut icon" href="data:image/x-icon;," type="image/x-icon">
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>{}</h1>
</body>
</html>
"""


class RedirectHandler(SimpleHTTPRequestHandler):
    """Sub class SimpleHTTPRequestHandler to handle redirect url."""

    def log_request(self, code='-', size='-'):
        """Ignore access log."""
        pass

    def do_GET(self):
        """Redirect url."""
        logging.info("got get request " + str(self.path))
        parsed_url = urlparse(self.path)
        query_string = parse_qs(parsed_url.query)
        code = query_string['code'][0]

        # persist code
        db.set("code", code)

        # response
        resp_text = "Authenticated successfully. You may now close this page."
        resp_html = RESP_SNIPPET.format(resp_text)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(resp_html.encode())

        self.server._BaseServer__shutdown_request = True


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """ThreadedTCPServer."""

    def handle_error(self, request, client_address):
        """Handle exception."""
        pass

    def __init__(self, server_address: Tuple[str, int], RequestHandlerClass: Callable[..., BaseRequestHandler]):
        self.allow_reuse_address = True
        super().__init__(server_address, RequestHandlerClass)


def get_local_server(host, port):
    """Run local server to listen for redirect url."""
    server = ThreadedTCPServer((host, port), RedirectHandler)
    return server
