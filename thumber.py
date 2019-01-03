'''Module contains a main entry point to run application'''
from dbus import SystemBus, Interface
from dbus.mainloop.glib import DBusGMainLoop
import gobject


class ThumbDriveDetector(object):
    '''
       Class wraps functionality to detect thumb drive.
    '''

    def __init__(self):
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

    def _is_removable_drive(self, data):
        '''
            Check if the added interface blpngs to some removable drive
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
        if interfaces_and_properties.get(self._drive_interface) is not None:
            if self._is_removable_drive(
                    interfaces_and_properties[self._drive_interface]):
                # Send email
                pass

    def detect(self):
        '''Starts main loop to detect thumb drive'''
        # Get UDisk2 DBUS object
        disk_systemd = self._bus.get_object(
            self._udisk2_interface, self._object_path)
        # Create an interface to work with object
        disk_manager = Interface(
            disk_systemd,
            dbus_interface=self._object_manager_interface)

        # Add callback to receive signal
        disk_manager.connect_to_signal(
            'InterfacesAdded', self._interface_added)

        # Create instance of main event loop and run it
        loop = gobject.MainLoop()
        loop.run()


if __name__ == "__main__":
    thumb_drive_detector = ThumbDriveDetector()
    thumb_drive_detector.detect()
