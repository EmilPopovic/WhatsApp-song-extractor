import requests
import json

_ = 'https://accounts.spotify.com/authorize?client_id=09a07ac5776a412aad2765a253cdacce&response_type=code&redirect_uri=https://example.com/&scope=playlist-modify-private%20playlist-modify-public'

CLIENT_ID = "09a07ac5776a412aad2765a253cdacce"
CLIENT_SECRET = "bdbe65258f7f46c194a7b81018bfa4cf"
REDIRECT_URI = "https://example.com/"
SCOPE = "playlist-modify-private playlist-modify-public"
ACCESS_TOKEN = "AQA57_2CJv5b3Wc-k4AQTAaIiZo-H0oOsIbfY0aww2D00iqa5grEeB9ehlpI98CwT3CdX1aNqy8dS0K7CooqhjIdj_SWZWf16EUAnNZpCqyD2aig_-BfeYVw1jq0LXwA82jkp99I8KDfXBwEQrt1kziR9-jz5KFjDGYpMjdBxQy_q4dfQJToPqI1NLr5kMHvVQrSmmh_eSlMiu-MTBFPBanQ_82JSoGroA"
REFRESH_TOKEN = ""
PLAYLIST_ID = "18pN98XFDp7i06iER8wDqC"


def read_video_urls(_=None):
    with open('extracted.csv', 'r') as f:
        contents = f.read()

    entries = contents.split('\n')

    urls = []

    for entry in entries[1:]:
        splt = entry.split(',')
        url = splt[3]
        urls.append(url)

    return urls


def get_authorization_token():
    auth_url = "https://accounts.spotify.com/authorize"
    token_url = "https://accounts.spotify.com/api/token"

    auth_payload = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
    }
    auth_response = requests.get(auth_url, params=auth_payload)
    auth_response.raise_for_status()

    auth_code = input(
        "Please authorize the app and enter the authorization code: "
    )

    token_payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
    }
    token_response = requests.post(token_url, data=token_payload)
    token_response.raise_for_status()

    token_data = token_response.json()
    global ACCESS_TOKEN
    ACCESS_TOKEN = token_data["access_token"]
    global REFRESH_TOKEN
    REFRESH_TOKEN = token_data["refresh_token"]




def create_playlist(name):
    url = f"https://api.spotify.com/v1/me/playlists"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "name": name,
        "public": False,  # Set to True for a public playlist
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    playlist_data = response.json()
    global PLAYLIST_ID
    PLAYLIST_ID = playlist_data["id"]
    print(f'Playlist id: {PLAYLIST_ID}')


def add_tracks_to_playlist(tracks):
    url = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    track_uris = [f"spotify:track:{track}" for track in tracks]
    payload = {"uris": track_uris}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.content)
    response.raise_for_status()


def main():
    playlist_name = "My Playlist"

    get_authorization_token()
    #create_playlist(playlist_name)

    video_urls = read_video_urls()

    track_ids = []
    for url in video_urls:
        track_id = url.split('track/')[1].split('?')[0]
        track_ids.append(track_id)

    batch_size = 100
    track_batches = [track_ids[i:i+batch_size] for i in range(0, len(track_ids), batch_size)]

    # Add tracks in batches
    for batch in track_batches:
        add_tracks_to_playlist(batch)


    print(f"Playlist '{playlist_name}' created successfully!")


if __name__ == "__main__":
    main()
