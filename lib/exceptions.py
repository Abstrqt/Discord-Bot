class SkyblockCommandError(Exception):
    """
    The base exception type for errors regarding user wrong skyblock-related input.
    """
    pass

class BadProfileError(SkyblockCommandError):
    """
    Exception raised when a user enters invalid profile name.
    """

    def __init__(self, profile):
        self.profile = profile


class NeverPlayedSkyblockError(SkyblockCommandError):
    """
    Exception raised when a user enters a player name/uuid that has never played skyblock before.
    """

    def __init__(self, uname):
        self.uname = uname


class APIDisabledError(SkyblockCommandError):
    """
    Exception raised when a user enters a player name/uuid that has their api disabled.
    """

    pass


class APIError(Exception):
    """
    The base exception type for errors regarding API.
    """
    pass

class InvalidIGN(APIError):
    """
    Exception raised when invalid ign given
    """
    def __init__(self, ign):
        self.ign = ign

class HypixelAPIThrottle(APIError):
    """
    Exception raised when hypixel api ratelimit is reached.
    """
    pass


class NotinDatabase(Exception):
    """
    Exception raised when user not in database
    """
    pass
