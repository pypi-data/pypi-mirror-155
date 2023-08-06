import logging

from celery import shared_task
from slack_sdk.web.client import WebClient

from . import exceptions

from django.conf import settings

logger = logging.getLogger(__name__)

client = WebClient(token=settings.SLACK_TOKEN)


# Since we typically deploy 2 workers and we don't want to go too
# much over the 1 message / second rate limit, we set our rate limit
# to 0.5 to be equivilant to 1 message / 2 seconds
# https://api.slack.com/docs/rate-limits#tier_t5
TASK_RATE_LIMIT = getattr(settings, "SLACK_RATE_LIMIT", 0.5)


# Wrapped version of Slack API Calll
# We want to make it easy to rate limit our calls to slack by wrapping
# it as a shared_task.
@shared_task(rate_limit=TASK_RATE_LIMIT)
def api_call(*args, **kwargs):
    try:
        return client.api_call(*args, json=kwargs).data
    except exceptions.SlackApiError as e:
        if e.response.data["error"] == "channel_not_found":
            raise exceptions.ChannelNotFound(
                kwargs.get("channel", "Unknown"), e.response
            ) from e
        if e.response.data["error"] == "is_archived":
            raise exceptions.ArchiveException(
                kwargs.get("channel", "Unknown"), e.response
            ) from e
        raise
