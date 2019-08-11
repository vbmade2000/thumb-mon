"""Contains a necessary functionality to implement logging mechanism
"""
import logging
import logging.handlers


# TODO: Make multiple logger and instantiate based on configuration
# TODO: Add format string to logger
# TODO: Make log-level configurable


class Logger(object):
    """Provide functionality to write logs.
       No support for formatters added yet.
    """

    def __init__(self, logger_name, log_level=logging.INFO, handlers=None):
        """Initialize class"""
        self._logger = logging.getLogger(logger_name)
        self._logger.setLevel(log_level)

        # Handler to log message to syslog
        handler = logging.handlers.SysLogHandler(address='/dev/log')
        self._logger.addHandler(handler)

        # Add handlers if any
        if handlers:
            for handler in handler:
                self._logger.addHandler(handler)

    def info(self, text):
        '''Logs info message'''
        if text:
            self._logger.info(text)

    def error(self, text):
        '''Logs error message'''
        if text:
            self._logger.error(text)

    def warning(self, text):
        '''Logs warning message'''
        if text:
            self._logger.warning(text)

    def debug(self, text):
        '''Logs debug message'''
        if text:
            self._logger.debug(text)

    def critical(self, text):
        '''Logs critical message'''
        if text:
            self._logger.critical(text)

    def exception(self, text):
        '''Logs exception message'''
        if text:
            self._logger.exception(text)
