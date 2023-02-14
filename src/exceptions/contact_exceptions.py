from src.exceptions.default_exception import DefaultException


class ContactAmountLimitException(DefaultException):
    """Exception raised when contact amount exceeds maximum amount."""

    default_message = "Contact amount limit exceeded"


class ContactAlreadyExistsException(DefaultException):
    """Exception raised when contact already exists."""

    default_message = "Contact already exists"
