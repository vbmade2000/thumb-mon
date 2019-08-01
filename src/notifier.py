"""Module contains an infrastructure to send notification using plugins.
"""

import importlib
import os


class Notifier(object):
    """Provides infrastructure to send notifications base on plugins.
    """

    CORE_SETTINGS_KEY = "CORE_SETTINGS"

    def __init__(self, config, logger):
        """Initializes class. Loads all configured plugins"""

        # Create a plugins directory from the current file path
        self._plugin_dir = os.path.abspath(
            os.path.join(os.path.realpath(__file__), "..", "plugins"))

        self._config = config
        self._loaded_plugins = None
        self._logger = logger
        self._plugin_names = self._config.get_value_list(
            self.CORE_SETTINGS_KEY, "output_plugins")
        self._loaded_plugin = list()
        self._load_plugins()

    def _load_plugins(self):
        """Imports plugin modules and instantiates plugin class"""

        # Optimization to avoid method name resolution every time
        append_instance = self._loaded_plugin.append

        # Iterate through plugin list. Import and instantiate each plugin
        # class
        for plugin_name in self._plugin_names:
            try:

                # Import module dynamically as per configuration
                # TODO: Check for directory name as plugin. There may be a
                #       case where plugin uses a multiple modules and so it
                #       is contained in a separate directory instead of single
                #       file.
                plugin_path = "src.plugins.{0}".format(plugin_name)
                imported_module = importlib.import_module(plugin_path)
                self._logger.info(
                    "Notifier: loaded plugin {0}".format(plugin_name))

                # We need plugin class name which is same as plugin file name
                # with title case.
                class_name = plugin_name.title()
                class_instance = getattr(imported_module, class_name)
                self._logger.info(
                    "Notifier: instantiated plugin {0}".format(plugin_name))

                append_instance(class_instance(self._config))

            except ImportError as _:
                # Handle ImportError here as we want to continue execution
                self._logger.error(
                    "Notifier: Error importing module {0}".format(plugin_name))
            except Exception as exception:
                # Raise any other exception
                raise exception

    def notify(self, alert_data):
        """Sends notifications using plugins"""
        self._logger.info("Sending notifications")

        # TODO: Use threads instead of going sequentially
        for loaded_plugin in self._loaded_plugin:
            loaded_plugin.send(alert_data)
