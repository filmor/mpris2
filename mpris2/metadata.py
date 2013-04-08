class MetadataWrapper():
    _data_map = {
        'track_id': 'mpris:trackid',
        'title': 'xesam:title',
        'track_number': 'xesam:trackNumber',
        'length': 'mpris:length',
        'genre': 'xesam:genre',
        'url': 'xesam:url',

        # Artist info
        'artist': 'xesam:artist',
        'album_artist': 'xesam:albumArtist',
        'composer': 'xesam:composer',
        'lyricist': 'xesam:lyricist',

        # Album info
        'art_url': 'mpris:artUrl',
        'album': 'xesam:album',
        'disc_number': 'xesam:discNumber',

        # Misc data
        'as_text': 'xesam:asText',
        'audio_bpm': 'xesam:audioBPM',
        'comment': 'xesam:comment',

        # Stats
        'content_created': 'xesam:content_created',
        'first_used': 'xesam:firstUsed',
        'last_used': 'xesam:lastUsed',
        'use_count': 'xesam:useCount',
        'user_rating': 'xesam:userRating',
        'auto_rating': 'xesam:autoRating',
    }

    _data = {}

    def __init__(self, data):
        self._data.update(data)

    def __str__(self):
        return str(self._data)

    __repr__ = __str__

    def __getitem__(self, item):
        if item in self._data_map:
            return self._data[self._data_map[item]]

    def __setitem__(self, key, value):
        raise KeyError('Metadata objects are read-only!')