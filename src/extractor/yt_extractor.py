import yt_dlp
from dataclasses import dataclass


@dataclass
class YtSongDto:
    def __init__(self, source: str, title: str, yt_id: str, artist: str):
        self.source = source
        self.title = title
        self.yt_id = yt_id
        self.artist = artist

    def __repr__(self) -> str:
        return f'title: {self.title}, author: {self.artist}'


class YtExtractor:
    YDL_OPTIONS = {
        'format': 'bestaudio',
        'audioquality': '0',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
        'geo_bypass': True,
        'skip_download': True,
        'youtube_skip_dash_manifest': True,
        'playlist_end': 1,
        'max_downloads': 1,
        'force_generic_extractor': True,
        'use-extractors': 'youtube',
        'external_downloader_args': ['-loglevel', 'panic']
    }
        
    @staticmethod
    def __extract_data(video: dict) -> tuple[str, str, str, str]:
        formats = video['formats']
        for f in formats:
            url = f['url']
            if 'googlevideo.com' in url:
                break
        else:
            url = None

        source = url
        title = video['title']
        yt_id = video['id']
        author_name = video['uploader']

        return source, title, yt_id, author_name

    @classmethod
    def by_url(cls, url: str) -> YtSongDto:
        with yt_dlp.YoutubeDL(cls.YDL_OPTIONS) as ydl:
            try:
                return YtSongDto(*cls.__extract_data(ydl.extract_info(url, download=False)))
            except Exception as _:
                raise ValueError(url)
