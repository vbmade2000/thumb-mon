"""Module contains a sample plugin that sends notification to syslog
"""

import time

from thumber.plugins.base_plugin import AbstractNotifier


class Plugin1(AbstractNotifier):
    """Sample plugin class that sends notification to syslog"""

    name = "Plugin1"

    def __init__(self, config=None, logger=None, msg_queue=None):
        """Initializes class"""
        super(Plugin1, self).__init__(config=config, logger=logger, msg_queue=msg_queue)

    def run(self):
        self._logger.error("Plugin1.run started")
        while True:
            msg = self._read_my_queue()
            self._logger.error("This is from Plugin1 => {0}".format(msg))
            time.sleep(4)

