"""Module contains a main entry point to run application"""

import os
import signal

from dbus import SystemBus, Interface
from dbus.mainloop.glib import DBusGMainLoop
import dbus
import gobject
import daemon

from thumber import logger
from thumber import notifier
from thumber.utils import config_reader


thumb_logger = logger.Logger("thumblogger")


# TODO: Move ThumbDriveDetector class to its own file
class ThumbDriveDetector(object):
    """
       Class wraps functionality to detect thumb drive.
    """

    def __init__(self, logger_instance, notifier_instance):
        """
            Initialize class
        """
        super(ThumbDriveDetector, self).__init__()
        self._logger = logger_instance
        self._logger.debug("ThumbDriveDetector.__init__ called")

        # Unblock main thread by calling this method.
        dbus.mainloop.glib.threads_init()

        # Set global default main loop
        DBusGMainLoop(set_as_default=True)

        self._udisk2_interface = 'org.freedesktop.UDisks2'
        self._object_manager_interface = 'org.freedesktop.DBus.ObjectManager'
        self._object_path = '/org/freedesktop/UDisks2'
        self._drive_interface = "org.freedesktop.UDisks2.Drive"
        self._bus = SystemBus()

        # Unblock main thread by calling this method.
        gobject.threads_init()
        # Create instance of main event loop and run it
        self._loop = gobject.MainLoop()

        self._notifier = notifier_instance
        self._logger.debug("Instantiated ThumbDriveDetector")

    def _is_removable_drive(self, data):
        """Check if the added interface belong to some removable drive
        based on value of some attribute(s).
        Removable drive has following attribute - value pairs which
        can be used to determine that media is removable.
        Removable: True
        Following are other useful attributes.
        TimeMediaDetected, Vendor, Optical, ConnectionBus, Ejectable,
        Model, Serial, Id, Size.

        Args:
            data (dict): Data received from DBUS for a device.

        Returns:
            bool: True if it is removable, False otherwise.
        """
        self._logger.debug("ThumbDriveDetector._is_removable_drive called")
        removable = data.get("Removable", False)
        return removable

    def _interface_added(self, _, interfaces_and_properties):
        """Callback method that gets triggered when new drive, job etc
           are added. It uses notifier object to notify to various channels.

        Args:
            _: Unused parameter. Ignore it.
            interfaces_and_properties (dict): Data related to device received
                from DBUS.
        """
        #  TODO: Create a separate class to store drive information
        self._logger.debug("ThumbDriveDetector._interface_added called")
        if interfaces_and_properties.get(self._drive_interface) is not None:
            if self._is_removable_drive(
                    interfaces_and_properties[self._drive_interface]):
                self._logger.debug("Detected removable drive")
                self._logger.debug(interfaces_and_properties)
                self._notifier.notify("Test data")

    def _run(self):
        """Starts main loop to detect thumb drive
        """
        # Get UDisk2 DBUS object
        disk_systemd = self._bus.get_object(
            self._udisk2_interface, self._object_path)
        self._logger.debug("Got UDisk2 DBUS object")
        # Create an interface to work with object
        disk_manager = Interface(
            disk_systemd,
            dbus_interface=self._object_manager_interface)
        self._logger.debug("Created interface to interact with object")

        # Add callback to receive signal
        disk_manager.connect_to_signal(
            'InterfacesAdded', self._interface_added)
        self._logger.debug("Added callback to signal")

        # Run main loop
        self._logger.info("Starting main loop")

        self._loop.run()

    def detect(self):
        self._run()

    def stop(self):
        """Stops the main loop
        """
        self._logger.info("Stopping main loop")
        self._loop.quit()


def signal_handler(signal, _):
    thumb_logger.info("Received SIGTERM, exiting...")
    exit(0)


def get_config_reader():
    # Create config reader
    # TODO: Get conf filepath from command line args. If it is supplied
    #       from command line then give it priority over file present in /etc.
    try:
        config_file_name = "thumber.conf"
        config_file_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), config_file_name)

        cfg_reader = config_reader.ConfigReader(config_file_path)
    except Exception as e:
        thumb_logger.error(e)
    return cfg_reader


def main():
    """Entry point"""
    # TODO: Put more debug statements
    # TODO: Send logs with print statement in exception handling
    # signal.signal(signal.SIGTERM, signal_handler)

    # Application demonizing process closes all the open file descriptors.
    # Here we have config file descriptor. So we moved out config reading
    # logic as we needed a config file descriptor to be passed in
    # DaemonContext context manager to prevent it from closing.
    cfg_reader = get_config_reader()

    with daemon.DaemonContext(
            files_preserve=[cfg_reader.get_config_file_descriptor()],
            signal_map={signal.SIGTERM: signal_handler}):

        try:
            # TODO: Make log level configurable
            # Create notifier
            event_notifier = notifier.Notifier(cfg_reader, logger=thumb_logger)
            thumb_drive_detector = ThumbDriveDetector(thumb_logger, event_notifier)
            thumb_drive_detector.detect()
            thumb_logger.info("Started thumber")

        except KeyboardInterrupt as _:
            # NOTE: \r can be used to remove ^C characters when printed to STDOUT.
            #       In syslog it prints like "[32B blob data]".
            thumb_logger.info("User requested exit. Exiting...")
        except config_reader.ConfigParser.NoSectionError as no_section_error:
            thumb_logger.error(
                "Config: section not found {0}".format(no_section_error.section))
        except Exception as exception:
            thumb_logger.error("Error: {0}".format(exception))

