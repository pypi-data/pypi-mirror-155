"""Exception."""


class CodeException(Exception):
    """Get code thread exception."""

    def __init__(self, exc_info):
        """Initialize the exception."""
        super().__init__(self)
        self.errorinfo = exc_info

    def __str__(self):
        """str."""
        return self.errorinfo


class TimeoutException(Exception):
    """Get code timeout exception."""

    def __init__(self, exc_info):
        """Initialize the exception."""
        super().__init__(self)
        self.errorinfo = exc_info

    def __str__(self):
        """str."""
        return self.errorinfo


class StoreNotFound(Exception):
    """Store not found exception."""

    def __init__(self, exc_info):
        """Initialize the exception."""
        super().__init__(self)
        self.errorinfo = exc_info

    def __str__(self):
        """str."""
        return self.errorinfo


class InvalidStore(Exception):
    """Invalide store exception."""

    def __init__(self, exc_info):
        """Initialize the exception."""
        super().__init__(self)
        self.errorinfo = exc_info

    def __str__(self):
        """str."""
        return self.errorinfo


class SameStore(Exception):
    """Raise when switch to the same store."""

    def __init__(self, exc_info):
        """Initialize the exception."""
        super().__init__(self)
        self.errorinfo = exc_info

    def __str__(self):
        """str."""
        return self.errorinfo


class CmdNotFound(Exception):
    """Raise when command not Found."""

    def __init__(self, exc_info):
        """Initialize the exception."""
        super().__init__(self)
        self.errorinfo = exc_info

    def __str__(self):
        """str."""
        return self.errorinfo


class NgrokInstallError(Exception):
    """Raise when ngrok installation failed."""

    def __init__(self, exc_info):
        """Initialize the exception."""
        super().__init__(self)
        self.errorinfo = exc_info

    def __str__(self):
        """str."""
        return self.errorinfo


class NgrokAuthError(Exception):
    """Raise when get ngrok authtoken failed."""

    def __init__(self, exc_info):
        """Initialize the exception."""
        super().__init__(self)
        self.errorinfo = exc_info

    def __str__(self):
        """str."""
        return self.errorinfo


class NgrokError(Exception):
    """Raise when ngrok log error."""

    def __init__(self, exc_info):
        """Initialize the exception."""
        super().__init__(self)
        self.errorinfo = exc_info

    def __str__(self):
        """str."""
        return self.errorinfo


class FetchUrlError(Exception):
    """Raise when fetch url from ngrok log timeout."""

    def __init__(self, exc_info):
        """Initialize the exception."""
        super().__init__(self)
        self.errorinfo = exc_info

    def __str__(self):
        """str."""
        return self.errorinfo


class NgrokNotRunning(Exception):
    """Raise when stop a not running ngrok tunnel."""

    def __init__(self, exc_info):
        """Initialize the exception."""
        super().__init__(self)
        self.errorinfo = exc_info

    def __str__(self):
        """str."""
        return self.errorinfo


class NgrokCannotStopped(Exception):
    """Raise when stop running ngrok failed."""

    def __init__(self, exc_info):
        """Initialize the exception."""
        super().__init__(self)
        self.errorinfo = exc_info

    def __str__(self):
        """str."""
        return self.errorinfo


class YamlDataError(Exception):
    """Raise when yaml file is not dict."""

    def __init__(self, exc_info):
        """Initialize the exception."""
        super().__init__(self)
        self.errorinfo = exc_info

    def __str__(self):
        """str."""
        return self.errorinfo


class NotInProjError(Exception):
    """Raise when yaml file is not dict."""

    def __init__(self, exc_info):
        """Initialize the exception."""
        super().__init__(self)
        self.errorinfo = exc_info

    def __str__(self):
        """str."""
        return self.errorinfo
