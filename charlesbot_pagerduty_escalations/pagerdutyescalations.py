from charlesbot.base_plugin import BasePlugin
from charlesbot.config import configuration
import asyncio


class PagerdutyEscalations(BasePlugin):

    def __init__(self):
        super().__init__("PagerdutyEscalations")
        self.load_config()

    def load_config(self):  # pragma: no cover
        config_dict = configuration.get()
        self.token = config_dict['pagerdutyescalations']['token']

    def get_help_message(self):
        return "!command - Does a neat thing!"

    @asyncio.coroutine
    def process_message(self, message):
        self.log.info("Processing message %s" % message)
