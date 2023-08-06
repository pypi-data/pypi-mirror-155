"""Simple key-value db."""
import os
import pickledb
from .context import get_cache_dir


class SimpleDB(object):
    """DB definition."""

    def __init__(self, db_path, auto_dump=True):
        """Init."""
        self.db_path = db_path
        try:
            self.db = pickledb.load(db_path, auto_dump)
        except Exception as e:
            print(e)

    def get(self, key):
        """Get value for key."""
        return self.db.get(key)

    def set(self, key, value):
        """Set value for key."""
        self.db.set(key, value)

    def delete(self, key):
        """Delete key."""
        self.db.rem(key)


db_path = os.path.join(
    os.path.realpath(get_cache_dir()), ".db.pstore"
)
db = SimpleDB(db_path)
