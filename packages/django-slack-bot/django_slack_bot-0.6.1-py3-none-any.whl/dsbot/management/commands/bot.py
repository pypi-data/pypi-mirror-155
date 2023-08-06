import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.test import override_settings

from dsbot.client import BotClient

try:
    from importlib.metadata import entry_points
except ImportError:
    from importlib_metadata import entry_points


class Command(BaseCommand):
    def add_arguments(self, parser):
        slack = parser.add_argument_group("Slack arguments")
        slack.add_argument("--token", default=settings.SLACK_TOKEN, help="Slack token")
        slack.add_argument("--timeout", default=30, type=int)
        slack.add_argument("--ping-interval", default=30, type=int)

        celery = parser.add_argument_group("Celery Arguments")
        celery.add_argument("--eager", action="store_true")

    def handle(self, verbosity, eager, **options):
        logging.root.setLevel(
            {
                0: logging.ERROR,
                1: logging.WARNING,
                2: logging.INFO,
                3: logging.DEBUG,
            }.get(verbosity)
        )

        ch = logging.StreamHandler()
        formatter = logging.Formatter(logging.BASIC_FORMAT)
        ch.setFormatter(formatter)

        logging.root.addHandler(ch)

        for entry in entry_points(group="dsbot.commands"):
            try:
                entry.load()
            except ImportError:
                logging.exception("Error loading %s", entry)
            else:
                logging.info("Loaded %s", entry)

        with override_settings(CELERY_TASK_ALWAYS_EAGER=eager):
            BotClient(
                token=options["token"],
                timeout=options["timeout"],
                ping_interval=options["ping_interval"],
            ).start()
