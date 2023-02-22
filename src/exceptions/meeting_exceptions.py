from src.exceptions.default_exception import DefaultException


class MeetingSlotsAlreadySelectedException(DefaultException):
    """Exception raised when user attempted to select slots again."""

    default_message = "Meeting slots already selected"
