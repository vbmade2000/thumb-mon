"""Module contains an abstract class that serves as base class for all
plugins.
"""

from abc import ABCMeta
from abc import abstractmethod


class AbstractNotifer(object):
    """Serves as a base class for all plugins"""

    __metaclass__ = ABCMeta

    def __init__(self):
        """Initialize class"""
        pass

    @abstractmethod
    def send(self):
        """Sends notification to particular channel implemented by plugin"""
        raise NotImplementedError
