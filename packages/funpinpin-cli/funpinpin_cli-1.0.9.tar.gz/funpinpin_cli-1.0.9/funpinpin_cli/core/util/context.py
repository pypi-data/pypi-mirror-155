"""Cli Context."""
import os
import platform
import pathlib
from funpinpin_cli.config import CLI_ENV

ROOT = os.getcwd()
TOOL_NAME = "funpinpin"
TOOL_FULL_NAME = "funpinpin CLI"
LOCALAPPDATA = os.getenv("LOCALAPPDATA", "")


def get_executable_file_extension(ext=".exe"):
    """Get executable file ext."""
    os = get_current_platform()
    if os == "windows":
        return ext
    return ""


def get_current_platform():
    """Get cli running os."""
    os = platform.system()
    if os == "Windows":
        return "windows"
    elif os == "Darwin":
        return "mac"
    elif os == "Linux":
        return "linux"
    return "unknown"


def get_cache_dir():
    """Get cache directory."""
    if CLI_ENV == "test":
        cache_dir = os.path.join(ROOT, ".tmp")
    elif LOCALAPPDATA:
        cache_dir = os.path.join(LOCALAPPDATA, TOOL_NAME)
    else:
        home = pathlib.Path.home()
        cache_dir = os.path.join(home, ".cache", TOOL_NAME)

    # Make sure the cache dir always exists
    pathlib.Path(cache_dir).mkdir(parents=True, exist_ok=True)

    return cache_dir


def which(cmd):
    """Return cmd path."""
    def is_exe(fpath):
        return (
            os.path.exists(fpath) and
            os.access(fpath, os.X_OK) and
            os.path.isfile(fpath)
        )

    def ext_candidates(fpath):
        yield fpath
        for ext in os.environ.get("PATHEXT", "").split(os.pathsep):
            yield fpath + ext

    fpath, fname = os.path.split(cmd)
    if not fpath:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, cmd)
            for candidate in ext_candidates(exe_file):
                if is_exe(candidate):
                    return candidate
    elif is_exe(cmd):
        return cmd

    return None


def linux(platform):
    """Return True if os == linux."""
    return platform == "linux"
