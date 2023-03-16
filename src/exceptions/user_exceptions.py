from src.exceptions.default_exception import DefaultException


class UserNotFoundException(DefaultException):
    """Exception raised when user not found."""
    default_message = "User not found"


class IncorrectModelException(DefaultException):
    """Exception raised when device is not android or ios."""

    default_message = "Device should be either android or ios"
