"""Module contains a sample plugin that just prints to stdout
"""

from src.plugins.base_plugin import AbstractNotifer


class Plugin1(AbstractNotifer):
    """Sample plugin class that prints notification to stdout"""

    def __init__(self, config):
        """Initializes class"""
        super(Plugin1, self).__init__(config)

    def send(self):
        """Prints notification to stdout"""
        setting = self._config.get_value("PLUGIN1", "sample_setting")
        print "Plugin1: Thumb drive detected {0}".format(setting)
