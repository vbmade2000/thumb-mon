"""Module contains an infrastructure to send notification using plugins.
"""


class Notifier(object):
    """Provides infrastructure to send notifications base on plugins.
    """

    def __init__(self, config, logger):
        '''Initializes class. Loads all configured plugins'''
        self._plugin_dir = None
        self._config = config
        self._loaded_plugins = None
        self._logger = logger
        self._loaded_plugins = config.get_value_list("CORE_SETTINGS", "output_plugins")
        self._logger.info(self._loaded_plugins)

    def notify(self, alert_data):
        """Sends notifications using plugins"""
        self._logger.info("Sending notifications")


