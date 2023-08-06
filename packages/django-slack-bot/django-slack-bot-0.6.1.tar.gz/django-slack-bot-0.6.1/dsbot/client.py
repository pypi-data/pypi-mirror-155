"""
Base Bot Class

The base bot class is mostly concerned with maintaining
the connection to Slack, and then dispatching events to
the Dispatcher

A few convenencie functions used by commands are also
added to the bot class
"""


import concurrent
import inspect
import logging
import re

import slack_sdk.rtm
import slack_sdk.web

from .exceptions import CommandError

logger = logging.getLogger(__name__)


class BotClient(slack_sdk.rtm.RTMClient):
    user_id = None
    _commands = []

    @classmethod
    def cmd(cls, key):
        """A decorator to store and link a callback to an event."""

        def decorator(callback):
            logger.debug("Registering %s %s", key, callback)
            cls._validate_callback(callback)
            cls._commands.append(
                {
                    "key": key,
                    "re": re.compile(key),
                    "func": callback,
                    "help": callback.__doc__.strip().split("\n")[0],
                }
            )
            return callback

        return decorator

    async def _dispatch_command(self, command, data=None):
        for cmd in self._commands:
            match = cmd["re"].match(command)
            if match:
                try:
                    if inspect.iscoroutinefunction(cmd["func"]):
                        logger.debug("Running %(key)s %(func)s as async", cmd)
                        return await cmd["func"](
                            rtm_client=self,
                            web_client=self._web_client,
                            data=data,
                            match=match,
                        )
                    else:
                        logger.debug("Running %(key)s %(func)s as thread", cmd)
                        self._cmd_in_thread(cmd["func"], data=data, match=match)
                except CommandError as e:
                    logger.warning("Command Error")
                    return self._web_client.chat_postEphemeral(
                        as_user=True,
                        channel=data["channel"],
                        user=data["user"],
                        attachments=[
                            {
                                "color": "warning",
                                "title": "Command Error",
                                "text": str(e),
                            }
                        ],
                    )
                except Exception as e:
                    logger.exception("Unknown Error")
                    return self._web_client.chat_postEphemeral(
                        as_user=True,
                        channel=data["channel"],
                        user=data["user"],
                        attachments=[
                            {
                                "color": "danger",
                                "title": "Unknown Error",
                                "text": str(e),
                            }
                        ],
                    )

    def _cmd_in_thread(self, callback, **kwargs):
        """Execute the callback in another thread. Wait for and return the results."""
        web_client = slack_sdk.web.WebClient(
            token=self.token,
            base_url=self.base_url,
            ssl=self.ssl,
            proxy=self.proxy,
            headers=self.headers,
        )
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                callback, rtm_client=self, web_client=web_client, **kwargs
            )

            while future.running():
                pass

            future.result()
