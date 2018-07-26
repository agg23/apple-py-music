# apple-music-py

Apple Music Python Client

Unofficial python wrapper for Apple Music API, not endorsed by Apple in any way

Subject to (frequent!) Apple Music API/documentation changes

https://developer.apple.com/documentation/applemusicapi

## Example Usage

```python
>>> from applemusicpy import AppleMusicClient

>>> client = AppleMusicClient('YOUR TEAM ID',
                              'YOUR KEY ID',
                              "-----BEGIN PRIVATE KEY-----\nYOUR KEY DATA HERE\n-----END PRIVATE KEY-----")

>>> client.get_songs_by_isrc('US2U61726301')
{u'data': [{u'attributes': {u'albumName': u'Bark Your Head Off, Dog',
    u'artistName': u'Hop Along',
    u'artwork': {u'bgColor': u'050505',
     u'height': 3000,
     u'textColor1': u'f3fcfb',
     u'textColor2': u'f7ccc6',
     u'textColor3': u'c3caca',
     u'textColor4': u'c6a49f',
     u'url': u'https://is3-ssl.mzstatic.com/image/thumb/Music118/v4/64/5f/98/645f9806-9a34-88ee-cebc-88fff9f25800/source/{w}x{h}bb.jpeg',
     u'width': 3000},
    u'discNumber': 1,
    u'durationInMillis': 228458,
    u'genreNames': [u'Alternative', u'Music', u'Rock'],
    u'isrc': u'US2U61726301',
    u'name': u'How Simple',
    u'playParams': {u'id': u'1334804732', u'kind': u'song'},
    u'previews': [{u'url': u'https://audio-ssl.itunes.apple.com/apple-assets-us-std-000001/AudioPreview128/v4/90/c4/c2/90c4c241-bfa8-4b16-6629-6c65e2d66fb0/mzaf_4354074312611241161.plus.aac.p.m4a'}],
    u'releaseDate': u'2018-04-06',
    u'trackNumber': 1,
    u'url': u'https://itunes.apple.com/us/album/how-simple/1334804729?i=1334804732'},
   u'href': u'/v1/catalog/us/songs/1334804732',
   u'id': u'1334804732',
   u'relationships': {u'albums': {u'data': [{u'href': u'/v1/catalog/us/albums/1334804729',
       u'id': u'1334804729',
       u'type': u'albums'}],
     u'href': u'/v1/catalog/us/songs/1334804732/albums'},
    u'artists': {u'data': [{u'href': u'/v1/catalog/us/artists/526442612',
       u'id': u'526442612',
       u'type': u'artists'}],
     u'href': u'/v1/catalog/us/songs/1334804732/artists'}},
   u'type': u'songs'}]}
```
