"""
These are the core commands and events that typically require a greater
knowledge about the internals of the bot itself
"""

import logging

from django.template.loader import render_to_string

from dsbot.client import BotClient
from dsbot.util import parse_direct_mention

logger = logging.getLogger(__name__)


@BotClient.cmd("^help")
async def cmd_help(rtm_client, web_client, data, **kwargs):
    """
    help - Show list of commands

    The help command loops through all registered dispatch commands and
    formats their help output via django's render_to_string method
    """
    return web_client.chat_postEphemeral(
        channel=data["channel"],
        as_user=True,
        text=render_to_string(
            "slack/response/help.txt", {"mapping": rtm_client._commands}
        ).strip(),
        user=data["user"],
    )


@BotClient.run_on(event="open")
async def get_team_data(rtm_client, data, **payload):
    rtm_client.user_id = data["self"]["id"]


@BotClient.run_on(event="message")
async def command_checker(web_client, rtm_client, data, **kwargs):
    """
    Basic command dispatch

    We want our bot to be a good citizen, so in public channels
    we only want it to respond to a direct @-mention

    In the case of direct private messages, we don't want to
    require @-mention, since it's obvious it's a command directly
    to the bot
    """
    if "subtype" in data:
        # https://api.slack.com/events/message#message_subtypes
        logger.debug("command_checker skips subtypes %s", data["subtype"])
        return

    # Check to see if this is an @ message
    user_id, message = parse_direct_mention(data["text"])

    if user_id == rtm_client.user_id:
        return await rtm_client._dispatch_command(message, data)
    # Or a direct message
    if data["channel"].startswith("D"):
        return await rtm_client._dispatch_command(data["text"], data)

    # Otherwise we ignore it to be a good citizen
    logger.debug("Ignoring non @ message in public channel %s", data)
