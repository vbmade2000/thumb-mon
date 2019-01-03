'''Module contains a main entry point to run application'''
import sys
import signal
from dbus import SystemBus, Interface
from dbus.mainloop.glib import DBusGMainLoop
import gobject
from src import logger


class ThumbDriveDetector(object):
    '''
       Class wraps functionality to detect thumb drive.
    '''

    def __init__(self, logger):
        '''
            Initialize class
        '''
        # Set global default main loop
        DBusGMainLoop(set_as_default=True)

        self._udisk2_interface = 'org.freedesktop.UDisks2'
        self._object_manager_interface = 'org.freedesktop.DBus.ObjectManager'
        self._object_path = '/org/freedesktop/UDisks2'
        self._drive_interface = "org.freedesktop.UDisks2.Drive"
        self._bus = SystemBus()
        # Create instance of main event loop and run it
        self._loop = gobject.MainLoop()
        self._logger = logger
        self._logger.debug("Instantiated ThumbDriveDetector")

    def _is_removable_drive(self, data):
        '''
            Check if the added interface belong to some removable drive
            based on value of some attribute(s).
            => Removale drive has following attribute - value pairs which
            can be used to determine that media is removable.
            Removable: True
            => Following are other useful attributes.
            TimeMediaDetected, Vendor, Optical, ConnectionBus, Ejectable,
            Model, Serial, Id, Size
        '''
        removable = data.get("Removable", False)
        return removable

    def _interface_added(self, _, interfaces_and_properties):
        '''Callback function that get triggered when new drive, job etc
           are added
        '''
        self._logger.debug("Interface added")
        if interfaces_and_properties.get(self._drive_interface) is not None:
            if self._is_removable_drive(
                    interfaces_and_properties[self._drive_interface]):
                self._logger.debug("Detected removable drive")
                # Send email
                pass

    def detect(self):
        '''Starts main loop to detect thumb drive'''
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
        '''Stops the main loop'''
        self._logger.info("Stopping main loop")
        self._loop.quit() 
        
def signal_handler(sig, frame):
    thumb_logger.info("User requested shutdown")
    thumb_drive_detector.stop()    
    thumb_logger.info("Exiting...")
    sys.exit(0)

thumb_logger = logger.Logger("thumblogger")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    thumb_drive_detector = ThumbDriveDetector(thumb_logger)
    thumb_logger.info("Started thumber")
    thumb_drive_detector.detect()
