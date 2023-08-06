class RundeckError(Exception):
    """Base class for all Rundeck exceptions"""

    pass


class VersionError(RundeckError):
    """Raised when the api version is not sufficient"""

    pass
