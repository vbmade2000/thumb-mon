"""Module contains a sample plugin that just prints to stdout
"""

import time

from src.plugins.base_plugin import AbstractNotifier


class Plugin1(AbstractNotifier):
    """Sample plugin class that prints notification to stdout"""

    def __init__(self, config=None, logger=None, msg_queue=None):
        """Initializes class"""
        super(Plugin1, self).__init__(config=config, logger=logger, msg_queue=msg_queue)

    def run(self):
        while True:
            self._logger.error("This is from Plugin1")
            time.sleep(4)

