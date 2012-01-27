'''
This is python mprisV2.1 documentation

http://www.mpris.org/2.1/spec/Playlists.html

'''
from pydbusdecorator.dbus_attr import DbusAttr
from pydbusdecorator.dbus_interface import DbusInterface
from pydbusdecorator.dbus_method import DbusMethod
from pydbusdecorator.dbus_signal import DbusSignal
from mpris2.interfaces import Interfaces
from mpris2.types import Playlist, Maybe_Playlist
from dbus import UInt32


@DbusInterface(Interfaces.PLAYLISTS, Interfaces.OBJECT_PATH)
class Playlists(Interfaces):
    '''
    Provides access to the media player's playlists.
    
    Since D-Bus does not provide an easy way to check for what interfaces are exported on an object, clients should attempt to get one of the properties on this interface to see if it is implemented.
    
    '''
    
    @DbusMethod
    def ActivatePlaylist(self, PlaylistId):
        '''
        **Parameters:**
        
        * PlaylistId - o
            The id of the playlist to activate.

        Starts playing the given playlist.
        
        Note that this must be implemented. If the media player does not allow clients to change the playlist, it should not implement this interface at all.
            
        It is up to the media player whether this completely replaces the current tracklist, or whether it is merely inserted into the tracklist and the first track starts. For example, if the media player is operating in a "jukebox" mode, it may just append the playlist to the list of upcoming tracks, and skip to the first track in the playlist.
        '''
        pass
    
    @DbusMethod(produces=lambda playlist_list: \
                    [Playlist(playlist) for playlist in playlist_list],
                args_to_dbus=[UInt32, UInt32, str, bool])
    def GetPlaylists(self, Index, MaxCount, Order, ReverseOrder=False):
        '''
        **Parameters:**
        
        * Index - u
            The index of the first playlist to be fetched (according to the ordering).
        * MaxCount - u
            The maximum number of playlists to fetch.
        * Order - s (Playlist_Ordering)
            The ordering that should be used.
        * ReverseOrder - b
            Whether the order should be reversed.

        **Returns**
        
        * Playlists - a(oss) (Playlist_List)
            A list of (at most MaxCount) playlists.
    
        Gets a set of playlists.
        '''
        pass
    
    @DbusSignal
    def PlaylistChanged(self, Playlist):
        '''
        **Parameters**
        
        * Playlist - (oss) (Playlist)
            The playlist whose details have changed.
    
        Indicates that the name or icon for a playlist has changed.
        
        Note that, for this signal to operate correctly, the id of the playlist must not change when the name changes.
        '''
        pass
    
    @DbusAttr
    def PlaylistCount(self):
        '''
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
    
        The number of playlists available.
        '''
        pass
    
    @DbusAttr
    def Orderings(self):
        '''
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
    
        The avaislable orderings. At least one must be offered.
        '''
        pass
    
    @DbusAttr(produces=Maybe_Playlist)
    def ActivePlaylist(self):
        '''
        **Returns**
        
        Read only
            When this property changes, the org.freedesktop.DBus.Properties.PropertiesChanged signal is emitted with the new value.
    
        The currently-active playlist.
        
        If there is no currently-active playlist, the structure's Valid field will be false, and the Playlist details are undefined.
        
        Note that this may not have a value even after ActivatePlaylist is called with a valid playlist id as ActivatePlaylist implementations have the option of simply inserting the contents of the playlist into the current tracklist.
        '''
        pass
    
if __name__ == '__main__':
    from mpris2.utils import SomePlayers
    uri = Interfaces.MEDIA_PLAYER + '.' + SomePlayers.RHYTHMBOX
    mp2 = Playlists(dbus_interface_info={'dbus_uri': uri})
    print mp2.ActivePlaylist
    print 'Active is valid playlist: ', bool(mp2.ActivePlaylist)
    if mp2.ActivePlaylist:
        print 'Active playlist name:', mp2.ActivePlaylist.Playlist.Name
    from mpris2.types import Playlist_Ordering
    print hasattr('anystring', 'eusequenaotem')
    print 'bla', mp2.GetPlaylists(0, 20, Playlist_Ordering.ALPHABETICAL, False)
    
    
    
    
    