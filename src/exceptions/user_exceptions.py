from src.exceptions.default_exception import DefaultException


class UserNotFoundException(DefaultException):
    """Exception raised when user not found."""
    default_message = "User not found"
