'''Module contains a main entry point to run application'''
from dbus import SystemBus, Interface
import gobject
from dbus.mainloop.glib import DBusGMainLoop


def _is_removable_drive(data):
    '''
        => Removale drive has following attribute - value pairs which can be
        used to determine that media is removable.
        Removable: True
        => Following are other useful attributes.
        TimeMediaDetected, Vendor, Optical, ConnectionBus, Ejectable, Model,
        Serial, Id, Size
    '''
    removable = data.get("Removable", False)
    if removable:
        print "Thumb drive found"
        return True
    return False


def interface_added(object_path, interfaces_and_properties):
    '''Callback function that get triggered when new drive, job etc is added'''
    print "Interface added"
    print "Object Path: %s" % object_path
    if interfaces_and_properties.get(
            "org.freedesktop.UDisks2.Drive") is not None:
        if _is_removable_drive(
                interfaces_and_properties["org.freedesktop.UDisks2.Drive"]):
            # Send email
            pass

# def interface_removed(object_path, interfaces):
#    print "Interface removed"


DBusGMainLoop(set_as_default=True)

udisk2_interface = 'org.freedesktop.UDisks2'
object_manager_interface = 'org.freedesktop.DBus.ObjectManager'
object_path = '/org/freedesktop/UDisks2'

bus = SystemBus()
disk_systemd = bus.get_object(udisk2_interface, object_path)
disk_manager = Interface(disk_systemd, dbus_interface=object_manager_interface)
# disk_manager.connect_to_signal('InterfacesRemoved', interface_removed)

# Add callback to receive signal
disk_manager.connect_to_signal('InterfacesAdded', interface_added)

# Create instance of main event loop and run it
loop = gobject.MainLoop()
loop.run()
