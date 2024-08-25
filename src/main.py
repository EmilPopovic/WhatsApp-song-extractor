import sys
import os
import re
from dotenv import load_dotenv
from datetime import datetime
from fuzzywuzzy import fuzz

from src.extractor import YtExtractor
from src.whatsapp import LinkFinder, Message
from extractor import SpotifyExtractor

FILENAME = '../data/backup_large.txt'
EXCLUDED_USERS = None
MINIMUM_SIMILARITY = 70

SPOTIFY_DOMAINS = [
    'https://open.spotify.com/track',
]

YT_DOMAINS = [
    'https://www.youtube.com/watch?v=',
    'https://youtube.com/watch?v=',
    'https://m.youtube.com/watch?v=',
    'https://youtu.be/',
]


def print_progress_bar(completed, total, length=50):
    # Calculate the progress
    progress = completed / total
    # Determine the number of filled characters in the bar
    filled_length = int(length * progress)
    # Create the bar string
    bar = '█' * filled_length + '-' * (length - filled_length)

    # Move the cursor up by one line and then to the beginning of the line
    sys.stdout.write('\033[F')  # ANSI escape code to move cursor up one line
    # Print the new bar, overwriting the previous bar
    sys.stdout.write(f'\r|{bar}| {completed}/{total} ({progress * 100:.2f}%)')
    sys.stdout.flush()


def main() -> None:
    messages = Message.parse_txt(FILENAME)

    platforms = input('Choose platforms to search (s - Spotify, y - YouTube, sy - Spotify and YouTube, a - all): ')

    supported_domains = []

    if 's' in platforms or 'a' in platforms:
        supported_domains.extend(SPOTIFY_DOMAINS)
    if 'y' in platforms or 'a' in platforms:
        supported_domains.extend(YT_DOMAINS)

    finder = LinkFinder(supported_domains)
    
    potentials: list[dict] = finder.get_urls(messages, EXCLUDED_USERS)

    print(f'Number of potentials: {len(potentials)}\n')

    print_potentials_check = input('Print potentials (y/n): ')

    if print_potentials_check == 'y':
        for potential in potentials:
            print(f'{potential['sender']} - {potential['url']}')

    continue_to_export_check = input('Continue? (y/n): ')

    if continue_to_export_check != 'y':
        sys.exit()

    load_dotenv('../.env')

    spotify = SpotifyExtractor(
        os.getenv('SPOTIFY_CLIENT_ID'),
        os.getenv('SPOTIFY_CLIENT_SECRET'),
        os.getenv('SPOTIFY_REDIRECT_URI'),
        os.getenv('SPOTIFY_SCOPE'),
    )

    create_playlist_check = input('Create playlist (y/n): ')

    if create_playlist_check == 'y':
        playlist_name = input('Playlist name: ')
        public = input('Public playlist (y/n): ')
        collaborative = input('Collaborative playlist (y/n): ')
        playlist_description = input('Playlist Description: ')

        playlist_id = spotify.create_playlist(playlist_name,
                                              public == 'y',
                                              collaborative == 'y',
                                              playlist_description)

    else:
        playlist_id = SpotifyExtractor.get_playlist_id_from_link(input('Playlist url: '))

    for i, potential in enumerate(potentials):
        print_progress_bar(i, len(potentials))

        url = potential['url']

        if url.startswith('https://open.spotify.com/track'):
            spotify.add_track_to_playlist(url, playlist_id)

        if any(url.startswith(domain) for domain in YT_DOMAINS):
            try:
                from_yt = YtExtractor.by_url(url)
            except ValueError:
                continue

            title = re.sub(r'\(.*?\)', '', from_yt.title)  # Remove anything in parentheses
            title = re.sub(r'\[.*?]', '', title)  # Remove anything in brackets
            title = re.sub(r'Official Video|Lyrics|Remix', '', title, flags=re.I)
            title.strip()

            combined_yt_info = f'{title} {from_yt.artist}'

            from_sp = spotify.get_track_from_search(f'{from_yt.title} {from_yt.artist}')

            sp_name = from_sp['name']
            sp_artist = from_sp['artists'][0]['name']

            combined_sp_info = f'{sp_name} {sp_artist}'

            match_ratio = fuzz.ratio(combined_yt_info.lower(), combined_sp_info.lower())

            if match_ratio > MINIMUM_SIMILARITY:
                spotify.add_track_to_playlist(spotify.uri_to_url(from_sp['uri']), playlist_id)

    print_progress_bar(len(potentials), len(potentials))


if __name__ == '__main__':
    start_time = datetime.now()

    main()

    end_time = datetime.now()
    delta = end_time - start_time
    print(f'\nTime taken: {str(delta)}')
