"""Module contains an abstract class that serves as base class for all
plugins.
"""

from abc import ABCMeta
from abc import abstractmethod
import threading


class AbstractNotifier(threading.Thread):
    """Serves as a base class for all plugins"""

    __metaclass__ = ABCMeta

    def __init__(self, config, logger, msg_queue):
        """Initialize class"""
        super(AbstractNotifier, self).__init__()
        self._config = config
        self._msg_queue = msg_queue
        self._logger = logger

    def _read_my_queue(self):
        msg = None
        try:
            msg = self._msg_queue.get()
        except Exception as exception:
            self._logger.exception(exception)
        return msg

    def _is_my_queue_empty(self):
        """Returns True/False based on empty status of _msg_queue"""
        q = self._msg_queue
        return q.empty()

    @abstractmethod
    def run(self):
        """Runs the thread"""
        raise NotImplementedError

    def get_name(self):
        """Returns a name of plugin"""
        return self.name
