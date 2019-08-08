"""Module contains an infrastructure to send notification using plugins.
"""

import importlib
import os
import Queue


class Notifier(object):
    """Provides infrastructure to send notifications base on plugins.
    """

    CORE_SETTINGS_KEY = "CORE_SETTINGS"

    def __init__(self, config, logger):
        """Initializes class. Loads all configured plugins"""
        self._logger.debug("Notifier.__init__ called")

        # Create a plugins directory from the current file path
        self._plugin_dir = os.path.abspath(
            os.path.join(os.path.realpath(__file__), "..", "plugins"))

        self._config = config
        self._loaded_plugins = None
        self._logger = logger
        self._plugin_names = self._config.get_value_list(
            self.CORE_SETTINGS_KEY, "output_plugins")
        self._loaded_plugin = list()
        self._queues = []  # List to hold queue reference for loaded plugins
        self._load_plugins()
        self._start_plugins()

    def _load_plugins(self):
        """Imports plugin modules and instantiates plugin class"""
        self._logger.debug("Notifier._load_plugins called")

        # Optimization to avoid method name resolution every time
        append_instance = self._loaded_plugin.append
        append_to_queue = self._queues.append

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

                # Create a new Queue for a plugin. Each plugin will have
                # its on queue.
                q = Queue.Queue()

                # Create an instance of loaded class and store it for further use
                append_instance(class_instance(
                    config=self._config, logger=self._logger, msg_queue=q))
                append_to_queue (q)

            except ImportError as _:
                # Handle ImportError here as we want to continue execution
                self._logger.error(
                    "Notifier: Error importing module {0}".format(plugin_name))
            except Exception as exception:
                # Raise any other exception
                raise exception

    def _start_plugins(self):
        """Starts all the loaded plugins"""
        self._logger.debug("Notifier._start_plugins called")
        self._logger.info("Started loading plugins")
        for loaded_plugin in self._loaded_plugin:
            loaded_plugin.setDaemon(True)
            loaded_plugin.start()
            self._logger.info("Loaded {0}".format(loaded_plugin.get_name()))

    def notify(self, alert_data):
        """Sends notifications using plugins"""
        self._logger.debug("Notifier.notify called")
        self._logger.info("Sending notifications")
        for q in self._queues:
            q.put("Sample Message from notifier")