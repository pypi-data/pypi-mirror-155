"""A simple process supervisor."""

import os
import subprocess
import time
from pathlib import Path
from signal import SIGTERM
import psutil

from ..util.context import (
    get_cache_dir, get_current_platform
)


class Supervision(object):
    """Supervision Class."""

    def __init__(
        self, identifier, pid=None, start_time=int(time.time())
    ):
        """Init."""
        self.identifier = identifier
        self.pid = pid
        self.start_time = start_time
        self.pid_path = os.path.join(self.run_dir(), f"{identifier}.pid")
        self.log_path = os.path.join(self.run_dir(), f"{identifier}.log")

    @classmethod
    def run_dir(cls):
        """Get current running directory."""
        run_dir = os.path.join(get_cache_dir(), "sv")
        Path(run_dir).mkdir(
            parents=True, exist_ok=True
        )
        return run_dir

    @classmethod
    def for_ident(cls, identifier):
        """Return supervisor single instance."""
        p_path = os.path.join(
            cls.run_dir(), f"{identifier}.pid"
        )
        try:
            with Path(p_path).open() as fd:
                content = fd.read()
            pid, start_time = content.split(":")
        except IOError:
            return None
        return Supervision(identifier, int(pid), start_time)

    @classmethod
    def is_running(cls, identifier):
        """Check if process is running."""
        process = cls.for_ident(identifier)
        if not process:
            return False
        return process.is_alive()

    def is_alive(self):
        """Whether process is alive."""
        return self.stat(self.pid)

    def stat(self, pid):
        """Check if process is alive."""
        return psutil.pid_exists(pid)

    def write(self):
        """Persist the pidfile."""
        Path(self.run_dir()).mkdir(parents=True, exist_ok=True)
        with Path(self.pid_path).open("w") as fd:
            fd.write(f"{self.pid}:{self.start_time}")

    @classmethod
    def start(cls, identifier, *args):
        """Start ngrok."""
        if cls.is_running(identifier):
            return cls.for_ident(identifier)

        sv = Supervision(identifier)
        fd_log = Path(sv.log_path).open("w")
        platform = get_current_platform()
        if platform == "windows":
            creation_flags = (
                subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
            )
            pid = subprocess.Popen(
                args,
                stdin=subprocess.DEVNULL,
                stdout=fd_log,
                stderr=fd_log,
                start_new_session=True,
                creationflags=creation_flags
            ).pid
        else:
            pid = subprocess.Popen(
                args,
                stdin=subprocess.DEVNULL,
                stdout=fd_log,
                stderr=fd_log,
                start_new_session=True,
            ).pid
        sv.pid = pid
        sv.write()
        time.sleep(1)
        return sv

    def del_pid(self):
        """Remove pid file."""
        Path(self.pid_path).unlink(missing_ok=True)

    @classmethod
    def stop(cls, identifier):
        """Stop ngrok."""
        process = cls.for_ident(identifier)
        if not process:
            return False
        return process.stop_daemon()

    def stop_daemon(self):
        """Stop the daemon."""
        try:
            while self.is_alive():
                os.kill(self.pid, SIGTERM)
                time.sleep(1)
        except OSError as e:
            err = str(e)
            if err.find("No such process") > 0:
                Path(self.pid_path).unlink(missing_ok=True)
                Path(self.log_path).unlink(missing_ok=True)
            else:
                print(err)
                return False
        Path(self.pid_path).unlink(missing_ok=True)
        Path(self.log_path).unlink(missing_ok=True)
        return True
