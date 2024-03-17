from lyricsgenius import Genius

GENIUS_API_KEY = 'RAYcEBxjXH4Wy7wnsITRJ7wW5iAbeecqFeG7nnPOwMW6QZoiSr85A2C1DDc3C78A'


class GeniusInfo:
    @staticmethod
    def get_lyrics(song_name: str, author_name: str) -> str:
        lyrics_genius = Genius(GENIUS_API_KEY)
        song_info = lyrics_genius.search_song(artist=author_name, title=song_name)
        lyrics = song_info.lyrics

        # remove junk in the beginning
        split_junk = lyrics.split('Lyrics')
        after_junk = ''.join(split_junk[1:])

        # remove junk in the end
        lyrics = after_junk.strip('You might also like50Embed')

        # clean text
        lyrics = lyrics.replace('`', "'")
        lyrics = lyrics.replace('"', '')

        if len(lyrics) > 3500:
            lyrics = None

        return lyrics
