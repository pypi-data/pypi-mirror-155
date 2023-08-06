"""Capture the current project that the user is working on."""
import os
import re

import pathlib
import yaml

from funpinpin_cli.core.util.exception import (
    YamlDataError, NotInProjError
)


class Project(object):
    """Project model."""

    def __init__(self):
        """Init."""
        self.at = self.dir = None

    def clear(self):
        """Clear."""
        self.at = self.dir = None

    def current(self, force_reload=False):
        """Get current project directory."""
        if force_reload:
            self.clear()
        return self.at(os.getcwd())

    def has_current(self):
        """Whether user in project directory."""
        if self.directory(self, os.getcwd()):
            return True
        return False

    def at(self, dir):
        """Get current project directory."""
        proj_dir = self.directory(dir)
        if not proj_dir:
            raise NotInProjError("not in a valid project directory.")
        if not self.at:
            self.at = {
                "dir": proj_dir
            }
        return self.at.get(proj_dir)

    def directory(self, dir):
        """Get current project directory."""
        if not self.dir:
            self.dir = {
                "dir": self.__directory(dir)
            }
        return self.dir.get(dir)

    def __directory(self, curr):
        while True:
            if curr == "/" or re.match(r"^[A-Z]:\/$", curr):
                return None
            yaml_file = os.path.join(curr, ".funpinpin-cli.yml")
            if pathlib.Path(yaml_file).exists():
                return curr
            curr = os.path.dirname(curr)

    def current_project_type(self):
        """Get the current project type."""
        if self.has_current():
            config = load_yaml_file(self.directory(), ".shopify-cli.yml")
            return config.get("project_type")
        return None


def load_yaml_file(directory, relative_path):
    """Load yaml file.

    Args:
        directory: project directory
        relative_path: yaml file
    """
    yaml_path = os.path.join()
    try:
        config = yaml.safe_load(yaml_path)
    except Exception as e:
        raise(e)

    if not isinstance(config, dict):
        raise YamlDataError("Yaml data is not dict.")
    return config
