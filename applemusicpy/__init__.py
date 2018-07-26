# -*- coding: utf-8 -*-

"""
Apple Music Python Client

Unofficial python wrapper for Apple Music API, not endorsed by Apple in any way

Subject to (frequent!) Apple Music API/documentation changes

Resources:
https://developer.apple.com/documentation/applemusicapi

HTTP Status Codes:
https://developer.apple.com/documentation/applemusicapi/http_status_codes
"""

import datetime
import jwt
import json
import requests


VERSION = '0.1.0'


BASE_URL = 'https://api.music.apple.com'

API_VERSION = 'v1'

TIMEOUT_SECONDS = 30


class AppleMusicClient(object):

    # Client-specific JSON Web Token
    # https://pyjwt.readthedocs.io/en/latest/
    # <str>
    developer_token = None

    def __init__(self, team_id, key_id, private_key, access_token=None,
                 base_url=BASE_URL, api_version=API_VERSION,
                 timeout=TIMEOUT_SECONDS):
        """
        Params:
            `team_id` <str>
            `key_id` <str>
            `private_key` <str> something like:
                "-----BEGIN PRIVATE KEY-----\nYOUR KEY DATA HERE\n-----END PRIVATE KEY-----"
            `access_token` <str>
            `base_url` <str>
            `api_version` <str>
            `timeout` <int>
        """
        self.team_id = team_id
        self.key_id = key_id
        self.private_key = private_key
        self.user_access_token = access_token
        self.base_url = base_url
        self.api_version = api_version
        self.timeout = timeout
        self.headers = self._get_auth_headers()

    def _get_auth_headers(self):
        self.developer_token = self._generate_developer_token(self.team_id,
                                                              self.key_id,
                                                              self.private_key)
        headers = {'Authorization': 'Bearer %s' % self.developer_token}
        if self.user_access_token:
            headers['Music-User-Token'] = self.user_access_token
        return headers

    def _generate_developer_token(self, team_id, key_id, private_key):
        algorithm = 'ES256'
        time_now = datetime.datetime.now()
        time_expired = time_now + datetime.timedelta(hours=12)
        payload = {
            'iss': team_id,
            'exp': int(time_expired.strftime('%s')),
            'iat': int(time_now.strftime('%s')),
        }
        headers = {
            'alg': algorithm,
            'kid': key_id,
        }
        return jwt.encode(payload,
                          private_key,
                          algorithm=algorithm,
                          headers=headers)

    def _request_method(self, method):
        return {
            'GET': requests.get,
            'POST': requests.post,
            'PUT': requests.put,
            'PATCH': requests.patch,
            'DELETE': requests.delete,
        }.get(method)

    def _make_request(self, method, endpoint, base_path=None, params=None,
                      payload=None):
        if base_path is None:
            base_path = "/%s" % self.api_version
        params = params or {}
        payload = payload or {}
        url = "%s%s%s" % (self.base_url, base_path, endpoint)
        request_method = self._request_method(method)
        result = request_method(url,
                                params=params,
                                headers=self.headers,
                                data=json.dumps(payload),
                                timeout=self.timeout)
        result.raise_for_status()
        return result and result.json() or {}

    """Helper Functions"""

    @property
    def access_token(self):
        return self.user_access_token

    @access_token.setter
    def access_token(self, value):
        self.headers['Music-User-Token'] = self.user_access_token = value

    def refresh_developer_token(self):
        self.headers = self._get_auth_headers()

    def next(self, resource, limit=None):
        """https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/RelationshipsandPagination.html#//apple_ref/doc/uid/TP40017625-CH135-SW1
        """
        if not (resource and resource.get('next')):
            return None
        params = {}
        if limit:
            params['limit'] = limit
        return self._make_request(
            method='GET',
            endpoint=resource.get('next'),
            base_path='',
            params=params,
        )

    """API Endpoints"""

    def search(self, query, limit=None, offset=None, storefront='us', types='songs'):
        """https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/Searchforresources.html#//apple_ref/doc/uid/TP40017625-CH58-SW1
        """
        if not query:
            return
        params = {'term': query}
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        if types:
            params['types'] = types
        return self._make_request(
            method='GET',
            endpoint="/catalog/%s/search" % storefront,
            params=params,
        )

    def get_song(self, id, storefront='us', include=None):
        """https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/GetaSingleSong.html#//apple_ref/doc/uid/TP40017625-CH22-SW1
        """
        params = {}
        if include:
            params['include'] = include
        return self._make_request(
            method='GET',
            endpoint="/catalog/%s/songs/%s" % (storefront, id),
            params=params,
        )

    def get_songs(self, ids, storefront='us', include=None):
        """https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/GetMultipleSongs.html#//apple_ref/doc/uid/TP40017625-CH30-SW1
        """
        params = {'ids': ','.join(ids)}
        if include:
            params['include'] = include
        return self._make_request(
            method='GET',
            endpoint="/catalog/%s/songs" % storefront,
            params=params,
        )

    def get_songs_by_isrc(self, isrc, storefront='us', include=None):
        """https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/GetMultipleSongs.html#//apple_ref/doc/uid/TP40017625-CH30-SW1
        """
        params = {'filter[isrc]': isrc}
        if include:
            params['include'] = include
        return self._make_request(
            method='GET',
            endpoint="/catalog/%s/songs" % storefront,
            params=params,
        )

    def get_playlist(self, id, storefront='us', include=None):
        """https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/GetaSinglePlaylist.html#//apple_ref/doc/uid/TP40017625-CH20-SW1
        """
        params = {}
        if include:
            params['include'] = include
        return self._make_request(
            method='GET',
            endpoint="/catalog/%s/playlists/%s" % (storefront, id),
            params=params,
        )

    def get_playlists(self, ids, storefront='us', include=None):
        """https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/GetMultiplePlaylists.html#//apple_ref/doc/uid/TP40017625-CH21-SW1
        """
        params = {'ids': ','.join(ids)}
        if include:
            params['include'] = include
        return self._make_request(
            method='GET',
            endpoint="/catalog/%s/playlists" % storefront,
            params=params,
        )

    def get_genre(self, id, storefront='us', include=None):
        """https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/GetaSingleGenres.html#//apple_ref/doc/uid/TP40017625-CH16-SW1
        """
        params = {}
        if include:
            params['include'] = include
        return self._make_request(
            method='GET',
            endpoint="/catalog/%s/genres/%s" % (storefront, id),
            params=params,
        )

    def get_genres(self, ids, storefront='us', include=None):
        """https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/GetMultipleGenres.html#//apple_ref/doc/uid/TP40017625-CH17-SW1
        """
        params = {'ids': ','.join(ids)}
        if include:
            params['include'] = include
        return self._make_request(
            method='GET',
            endpoint="/catalog/%s/genres" % storefront,
            params=params,
        )

    def user_playlist_create(self, name, description=None, tracks=None,
                             include=None):
        """
        Params:
            `name` <str>
            `description` <str>
            `tracks` <list(
                # https://developer.apple.com/documentation/applemusicapi/libraryplaylistrequesttrack
                <dict{
                    'id': <str> (Required) The unique identifier for the track.
                        This ID can be a catalog identifier or a library
                        identifier, depending on the track type.
                    'type': <str> (Required) The type of the track to be added.
                        The possible values are songs, music-videos,
                        library-songs, or library-music-videos.
                }>,
                ...
            )>
            # TODO: Example(s) of `include`?
            `include` <str> Additional relationships to include in the fetch.

        https://developer.apple.com/documentation/applemusicapi/create_a_new_library_playlist
        """
        params = {}
        payload = {}
        # https://developer.apple.com/documentation/applemusicapi/libraryplaylistcreationrequest
        # https://developer.apple.com/documentation/applemusicapi/libraryplaylistcreationrequest/attributes
        payload['attributes'] = {'name': name}
        if description:
            payload['attributes']['description'] = description
        if tracks:
            # https://developer.apple.com/documentation/applemusicapi/libraryplaylistcreationrequest/relationships
            # https://developer.apple.com/documentation/applemusicapi/libraryplaylistrequesttrack
            payload['relationships']['tracks'] = tracks
        if include:
            params['include'] = include
        return self._make_request(
            method='POST',
            endpoint='/me/library/playlists',
            params=params,
            payload=payload,
        )

    def user_playlist_update(self, id, name=None, description=None):
        """https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/UpdateLibraryPlaylistAttributes.html#//apple_ref/doc/uid/TP40017625-CH248-SW1
        """
        payload = {
            'attributes': {}
        }
        if name:
            payload['attributes']['name'] = name
        if description:
            payload['attributes']['description'] = description
        return self._make_request(
            method='PATCH',
            endpoint="/me/library/playlists/%s" % id,
            payload=payload,
        )

    def user_playlist_delete(self, id):
        """https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/DeleteLibraryPlaylist.html#//apple_ref/doc/uid/TP40017625-CH244-SW1
        """
        return self._make_request(
            method='DELETE',
            endpoint="/me/library/playlists/%s" % id,
        )

    def user_playlist_add_tracks(self, id, track_ids):
        """https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/AddTracktoLibraryPlaylist.html#//apple_ref/doc/uid/TP40017625-CH249-SW1
        """
        payload = {
            'data': []
        }
        for track_id in track_ids:
            payload['data'].append({
                'id': str(track_id),
                'type': 'songs',
            })
        return self._make_request(
            method='POST',
            endpoint="/me/library/playlists/%s/tracks" % id,
            payload=payload,
        )

    def user_playlist_replace_tracks(self, id, track_ids):
        """https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/ReplaceTracklistforLibraryPlaylist.html#//apple_ref/doc/uid/TP40017625-CH250-SW1
        """
        payload = {
            'data': []
        }
        for track_id in track_ids:
            payload['data'].append({
                'id': str(track_id),
                'type': 'songs',
            })
        return self._make_request(
            method='PUT',
            endpoint="/me/library/playlists/%s/tracks" % id,
            payload=payload,
        )

    def user_playlist_remove_tracks(self, id, track_ids):
        """https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/DeleteTrackfromLibraryPlaylist.html#//apple_ref/doc/uid/TP40017625-CH251-SW1
        """
        params = {
            'ids[library-songs]': [str(track_id) for track_id in track_ids],
            'mode': 'all',
        }
        return self._make_request(
            method='DELETE',
            endpoint="/me/library/playlists/%s" % id,
            params=params,
        )

    def user_playlist(self, id, include=None):
        """https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/GetaSingleLibraryPlaylist.html#//apple_ref/doc/uid/TP40017625-CH212-SW1
        """
        params = {}
        if include:
            params['include'] = include
        return self._make_request(
            method='GET',
            endpoint="/me/library/playlists/%s" % id,
            params=params,
        )

    def user_playlists(self, limit=None, include=None):
        """https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/GetAllLibraryPlaylists.html#//apple_ref/doc/uid/TP40017625-CH216-SW1
        """
        params = {}
        if limit:
            params['limit'] = limit
        if include:
            params['include'] = include
        return self._make_request(
            method='GET',
            endpoint='/me/library/playlists',
            params=params,
        )

    def user_heavy_rotation(self, limit=None, offset=None):
        """https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/GetHeavilyRotated.html#//apple_ref/doc/uid/TP40017625-CH63-SW1
        """
        params = {}
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        return self._make_request(
            method='GET',
            endpoint='/me/history/heavy-rotation',
            params=params,
        )

    def user_recent_played(self, limit=None, offset=None):
        """https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/GetRecentlyPlayed.html#//apple_ref/doc/uid/TP40017625-CH62-SW1
        """
        params = {}
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        return self._make_request(
            method='GET',
            endpoint='/me/recent/played',
            params=params,
        )

    def user_recent_added(self, limit=None, offset=None):
        """https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/GetRecentlyAdded.html#//apple_ref/doc/uid/TP40017625-CH226-SW1
        """
        params = {}
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        return self._make_request(
            method='GET',
            endpoint='/me/library/recently-added',
            params=params,
        )

    def user_songs(self, limit=None, include=None):
        """https://developer.apple.com/library/content/documentation/NetworkingInternetWeb/Conceptual/AppleMusicWebServicesReference/GetAllLibrarySongs.html#//apple_ref/doc/uid/TP40017625-CH217-SW1
        """
        params = {}
        if limit:
            params['limit'] = limit
        if include:
            params['include'] = include
        return self._make_request(
            method='GET',
            endpoint='/me/library/songs',
            params=params,
        )
