"""REST API Light Exceptions"""

class RestLightException(Exception):
    """General REST Light Exception."""

class Unavailable(RestLightException):
    """Device is unavailable."""

class InvalidEffect(RestLightException, ValueError):
    """Invalid effect specified."""