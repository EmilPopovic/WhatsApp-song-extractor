import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyExtractor:

    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 redirect_uri: str,
                 scope: str) -> None:
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(client_id=client_id,
                                      client_secret=client_secret,
                                      redirect_uri=redirect_uri,
                                      scope=scope))

    def print_saved_tracks(self):
        results = self.sp.current_user_saved_tracks()
        for i, item in enumerate(results['items']):
            track = item['track']
            print(i, track['artists'][0]['name'], " – ", track['name'])

    def create_playlist(self,
                        playlist_name: str,
                        public: bool = True,
                        collaborative: bool = False,
                        description: str = '') -> str:
        playlist = self.sp.user_playlist_create(self.sp.me()['id'],
                                                playlist_name,
                                                public=public,
                                                collaborative=collaborative,
                                                description=description)
        return playlist['id']

    def add_track_to_playlist(self, track_url: str, playlist_id: str) -> None:
        track_id = track_url.split('/')[-1]
        if '?' in track_id:
            track_id = track_id.split('?')[0]

        track_info = self.sp.track(track_id)
        self.sp.playlist_add_items(playlist_id, [track_info['uri']])

    def add_tracks_to_playlist(self, track_urls: list[str], playlist_id: str) -> None:
        for track_url in track_urls:
            self.add_track_to_playlist(track_url, playlist_id)

    @staticmethod
    def get_playlist_id_from_link(playlist_url: str) -> str:
        if '/playlist/' in playlist_url:
            playlist_id = playlist_url.split('/playlist/')[-1]
        else:
            raise ValueError("Invalid Spotify playlist url")

        if '?' in playlist_id:
            playlist_id = playlist_id.split('?')[0]

        return playlist_id

    def get_track_from_search(self, query: str) -> dict:
        results = self.sp.search(q=query, type='track', limit=1)

        if not results['tracks']['items']:
            raise ValueError('No tracks found')

        return results['tracks']['items'][0]

    @staticmethod
    def uri_to_url(uri: str) -> str:
        url = uri.replace('spotify:', 'https://open.spotify.com/')
        url = url.replace(':', '/')
        return url
