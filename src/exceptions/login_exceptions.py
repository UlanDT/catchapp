from src.exceptions.default_exception import DefaultException


class OtpVerificationException(DefaultException):
    """Exception raised when otp code is not correct OR if otp expired."""
    default_message = "Что то пошло не так"
