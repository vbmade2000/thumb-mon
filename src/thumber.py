"""Module contains a main entry point to run application"""

from dbus import SystemBus, Interface
from dbus.mainloop.glib import DBusGMainLoop
import gobject

from src import logger, notifier


class ThumbDriveDetector(object):
    """
       Class wraps functionality to detect thumb drive.
    """

    def __init__(self, logger_instance, notifier_instance):
        """
            Initialize class
        """

        # Set global default main loop
        DBusGMainLoop(set_as_default=True)

        self._udisk2_interface = 'org.freedesktop.UDisks2'
        self._object_manager_interface = 'org.freedesktop.DBus.ObjectManager'
        self._object_path = '/org/freedesktop/UDisks2'
        self._drive_interface = "org.freedesktop.UDisks2.Drive"
        self._bus = SystemBus()

        # Create instance of main event loop and run it
        self._loop = gobject.MainLoop()
        self._logger = logger_instance
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
        self._logger.debug("Interface added")
        if interfaces_and_properties.get(self._drive_interface) is not None:
            if self._is_removable_drive(
                    interfaces_and_properties[self._drive_interface]):
                self._logger.debug("Detected removable drive")
                self._notifier.notify("Test data")

    def detect(self):
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

    def stop(self):
        """Stops the main loop
        """
        self._logger.info("Stopping main loop")
        self._loop.quit()


def main():
    """Entry point"""
    try:
        thumb_logger = logger.Logger("thumblogger")
        event_notifier = notifier.Notifier(thumb_logger, None)
        thumb_drive_detector = ThumbDriveDetector(thumb_logger, event_notifier)
        thumb_logger.info("Started thumber")
        thumb_drive_detector.detect()
    except KeyboardInterrupt as _:
        print "User requested exit. Exiting..."
    except Exception as exception:
        print "Error: {0}".format(exception)


if __name__ == "__main__":
    main()