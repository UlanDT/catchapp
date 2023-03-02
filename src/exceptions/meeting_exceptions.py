from src.exceptions.default_exception import DefaultException


class MeetingSlotsAlreadySelectedException(DefaultException):
    """Exception raised when user attempted to select slots again."""

    default_message = "Meeting slots already selected"


class MeetingNotReadyException(DefaultException):
    """Exception raised when user attempted to call contact when meeting is not ready yet."""

    default_message = "Meeting not ready yet"
