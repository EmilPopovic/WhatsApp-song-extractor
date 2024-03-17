class YTDLError(Exception):
    def __init__(self, query):
        print(f'YouTube extract errof for: {query}')
        pass


class SpotifyExtractError(Exception):
    def __init__(self, err=None):
        if err:
            print(f'Spotify extract error')
