"""Module contains a sample plugin that just prints to stdout
"""

from src.plugins.base_plugin import AbstractNotifer


class Plugin1(AbstractNotifer):
    """Sample plugin class that prints notification to stdout"""

    def __init__(self):
        """Initializes class"""
        super(Plugin1, self).__init__()

    def send(self):
        """Prints notification to stdout"""
        print "Plugin1: Thumb drive detected"
