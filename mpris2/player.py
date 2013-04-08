import dbus

from mpris2.dbusobject import DbusObject
from mpris2.metadata import MetadataWrapper
from mpris2.utils import enum


_main_interface = 'org.mpris.MediaPlayer2'

def get_all(bus=dbus.SessionBus()):
    proxy = bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus')
    for item in proxy.ListNames(dbus_interface='org.freedesktop.DBus'):
        if item.startswith(_main_interface):
            yield Player(item, bus)


PlaybackStatus = enum('PlaybackStatus',
                      'Playing',
                      'Paused',
                      'Stopped',
)

LoopStatus = enum('LoopStatus',
                  'Track',
                  'Playlist',
                  'None'
)


class Player(DbusObject):
    def __init__(self, bus_name, bus):
        super().__init__(bus_name, '/org/mpris/MediaPlayer2', [_main_interface, 'org.mpris.MediaPlayer2.Player', 'org.mpris.MediaPlayer2.TrackList', 'org.mpris.MediaPlayer2.Playlists'], bus)

    @property
    def Metadata(self):
        return MetadataWrapper(self._get_dbus_attr('Metadata'))