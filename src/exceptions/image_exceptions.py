from src.exceptions.default_exception import DefaultException


class ImageNotFoundException(DefaultException):
    """Exception raised when image is not found"""
    default_message = "Image not found"
