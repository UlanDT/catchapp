class DefaultException(Exception):
    """Base exception."""
    default_message = 'Something went wrong'

    def __init__(self, message=None):
        self.message = message if message else self.default_message
