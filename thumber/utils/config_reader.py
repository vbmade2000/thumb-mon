"""Configuration file reader
"""

import ConfigParser


class ConfigReader(object):
    """Configuration reader
    """

    def __init__(self, config_filename):
        """Initialize ConfigReader
        """
        self._config_parser = ConfigParser.RawConfigParser()
        self._config_file_descriptor = open(config_filename)
        self._config_parser.readfp(self._config_file_descriptor)

    def get_value(self, section, key):
        """Read a single value of a <key> from a <section>.

        Args:
            section (str): Section of the configuration file to read from.
            key (str): Key who value you want to read.

        Returns:
            str: Value
        """
        value = self._config_parser.get(section, key)
        if value == [""]:
            value = ""
        return value

    def get_value_list(self, section, key):
        """Read a list of values of a <key> from a <section>.

        Args:
            section (str): Section of the configuration file to read from.
            key (str): Key who value you want to read.

        Returns:
            list: List of values.
        """
        values = []
        value = self.get_value(section, key)
        if value != "":
            raw_values = value.split(",")
            values = [val.strip() for val in raw_values]
        return values

    def get_config_file_descriptor(self):
        return self._config_file_descriptor