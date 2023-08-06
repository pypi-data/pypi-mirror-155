"""Cli tunnel."""
import os
import time
import re
import pathlib
import requests

from .util.simple_supervision import Supervision
from .util.exception import (
    CmdNotFound, NgrokInstallError, NgrokAuthError,
    NgrokError, FetchUrlError, NgrokNotRunning,
    NgrokCannotStopped
)
from .util.context import (
    get_executable_file_extension, get_cache_dir,
    get_current_platform, which, linux
)


class Tunnel(object):
    """Tunnel interface."""

    # mapping for supported operating systems for where to download ngrok from.
    DOWNLOAD_URLS = {
        "mac": "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-darwin-amd64.zip",
        "mac_m1": "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-darwin-arm64.zip",
        "linux": "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip",
        "windows": "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip",
    }

    PORT = 8081  # port that ngrok will bind to

    NGROK_TUNNELS_URI = "http://localhost:4040/api/tunnels"
    TUNNELS_FIELD = "tunnels"
    PUBLIC_URL_FIELD = "public_url"

    @classmethod
    def fetch_url(cls, log_path):
        """Fetch account and url."""
        log = LogParser(log_path)
        account, url = log.do()
        return account, url

    @classmethod
    def install(cls):
        """Download and install ngrok to cache dir."""
        # check if ngrok had been downlodaed.
        if pathlib.Path(cls.ngrok_path()).exists():
            return

        # if not intalled, download.
        # check if curl, unzip, or tar is installed.
        platform = get_current_platform()
        cls.check_prereq_command("curl")
        cls.check_prereq_command("unzip" if linux(platform) else "tar")

        # using curl to download ngrok
        cache_dir = get_cache_dir()
        os.chdir(cache_dir)
        if not pathlib.Path("ngrok.zip").exists():
            src_url = Tunnel.DOWNLOAD_URLS[platform]
            cmd = f"curl -o ngrok.zip {src_url}"
            os.system(cmd)

        # unzip ngrok.zip
        if linux(platform):
            cmd = "unzip -u ngrok.zip"
        else:
            cmd = "tar -xf ngrok.zip"
        os.system(cmd)

        # rm zip
        pathlib.Path("ngrok.zip").unlink(missing_ok=True)

        if not pathlib.Path(cls.ngrok_path()).exists():
            raise NgrokInstallError("download and install ngrok failed.")
        print("Installing ngrok…")

    @classmethod
    def auth(cls, token):
        """Install ngrok and config token."""
        cls.install()
        os.chdir(get_cache_dir())
        cmd = " ".join(["ngrok", "authtoken", token])
        os.system(cmd)

    @classmethod
    def authenticated(cls):
        """Check if ngrok is authenticated."""
        home = pathlib.Path.home()
        ngrok_config_path = os.path.join(home, ".ngrok2/ngrok.yml")
        ng_path = pathlib.Path(ngrok_config_path)
        if not ng_path.exists():
            return False
        with ng_path.open() as fd:
            content = fd.read()
            if "authtoken" in content:
                return True
        return False

    @classmethod
    def start(cls, port):
        """Start ngrok.

        Args:
            port: port to use to open the ngrok tunnel
        Returns:
            url: url that the tunnel is bound to and available to the public
        """
        cls.install()
        if not cls.authenticated():
            raise NgrokAuthError("ngrok account authtoken error.")
        url, account = cls.start_ngrok(port or Tunnel.PORT)
        return url, account

    @classmethod
    def stop(cls):
        """Strop ngrok."""
        identifier = cls.ngrok_identifier()
        if Supervision.is_running(identifier):
            if Supervision.stop(identifier):
                return
            else:
                raise NgrokCannotStopped("ngrok tunnel can not stop")
        else:
            raise NgrokNotRunning("ngrok tunnel not running")

    @classmethod
    def ngrok_identifier(cls):
        """Return identifier."""
        return f"ngrok{get_executable_file_extension()}"

    @classmethod
    def ngrok_path(cls):
        """Get ngrok full path."""
        cache_dir = get_cache_dir()
        ngrok_path = os.path.join(cache_dir, cls.ngrok_identifier())
        return ngrok_path

    @classmethod
    def ngrok_command(cls, port):
        """Format ngrok command."""
        ngrok_path = cls.ngrok_path()
        ngrok_cmd = [
            ngrok_path, "http", "--inspect=false",
            "--log=stdout", "--log-level=debug", str(port)
        ]
        return ngrok_cmd

    @classmethod
    def start_ngrok(cls, port):
        """Start ngrok."""
        ngrok_cmd = cls.ngrok_command(port)
        process = Supervision.start(cls.ngrok_identifier(), *ngrok_cmd)
        account, url = cls.fetch_url(process.log_path)
        return account, url

    @classmethod
    def stats(cls):
        """Send get request to local ngrok server."""
        try:
            resp = requests.get(cls.NGROK_TUNNELS_URI)
            return resp.json()
        except Exception as e:
            return {}

    @classmethod
    def urls(cls):
        """Get tunnel public urls."""
        tunnels = cls.stats().get(cls.TUNNELS_FIELD, [])
        urls = []
        for tunnel in tunnels:
            i = tunnel.get(cls.PUBLIC_URL_FIELD)
            if i:
                urls.append(i)
        return urls

    @classmethod
    def check_prereq_command(cls, cmd):
        """Check if cmd is installed."""
        cmd_path = which(cmd)
        if cmd_path:
            print(f"{cmd} @ {cmd_path}")
        if not cmd:
            raise CmdNotFound(f"{cmd} is not installed.")


class LogParser(object):
    """Log parser."""

    TIMEOUT = 10

    def __init__(self, log_path):
        """Init."""
        self.log_path = log_path

    def do(self):
        """Begin analize ngrok log."""
        counter = 0
        while counter < self.TIMEOUT:
            account, url = self.parse()
            if url:
                return account, url
            counter += 1
            time.sleep(1)
        raise FetchUrlError("fetch url timeout.")

    def parse(self):
        """Get account and url from ngrok log."""
        p_log = pathlib.Path(self.log_path)
        content = ""
        with p_log.open() as fd:
            content = fd.read()
        self.parse_error(content)
        account = self.parse_account(content)
        url = self.parse_url(content)
        return account, url

    def parse_error(self, log):
        """Extract error from log."""
        match = re.search(
            r"msg=\"command failed\" err=\"([^\"]+)\"",
            log
        )
        if match:
            raise NgrokError(match.group(1))

    def parse_account(self, log):
        """Extract account from log."""
        match = re.search(
            r"AccountName:(.*)\s+SessionDuration",
            log
        )
        if match:
            return match.group(1)
        return None

    def parse_url(self, log):
        """Extract url from log."""
        match = re.search(
            r"msg=\"started tunnel\".*url=(https:\/\/.+)",
            log
        )
        if match:
            return match.group(1)
        return None
