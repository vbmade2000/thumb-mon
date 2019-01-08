'''Module contains an infrastructure to send notification using plugins.
'''

class Notifier(object):
    '''Provides infrastructure to send notifications base on plugins.
    '''

    def __init__(self, config, logger):
        '''Initializes class. Loads all configured plugins'''
        self._plugin_dir = None
        self._config = config

    def notify(self, alert_data):
        '''Sends notifications using plugins'''
        logger.info("Sending notifications") 


