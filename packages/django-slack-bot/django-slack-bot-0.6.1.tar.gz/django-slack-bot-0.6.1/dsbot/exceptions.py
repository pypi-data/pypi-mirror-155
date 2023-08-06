from slack_sdk.errors import SlackApiError


class BaseException(Exception):
    pass


class CommandError(BaseException):
    pass


class ArgumentError(CommandError):
    pass


# Custom slack exceptions


class ArchiveException(SlackApiError):
    pass


class ChannelNotFound(SlackApiError):
    pass


class SlackException(BaseException):
    def __init__(self, response):
        self.data = response

    def __str__(self):
        return self.data["error"]

    def __repr__(self):
        return "SlackException(%s)" % self
