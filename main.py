from difflib import SequenceMatcher
from datetime import datetime

from message_search import get_urls
from utils import *
from song_generator import SongGenerator as Song

FILENAME = 'backup.txt'
EXCLUDED_USERS = None
MINIMUM_SIMILARITY = 0.3


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def print_progress_bar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print()
        print()


def reset_files():
    with open('with_error.txt', 'w') as f:
        f.write('')

    with open('not_similar.txt', 'w') as f:
        f.write('')

    with open('extracted.txt', 'w') as f:
        f.write('')

    with open('extracted.csv', 'w') as f:
        f.write('')


def main():
    with open('counter.txt', 'r') as f:
        n = int(f.read())

    if n == -1:
        reset_files()
    
    potentials = get_urls(FILENAME, EXCLUDED_USERS)[n+1:]

    num_of_potentials = len(potentials)

    print(f'Number of potentials: {num_of_potentials}\n')

    songs = 0
    with_error = 0
    not_similar = 0

    for i, potential in enumerate(potentials):
        with open('counter.txt', 'w') as f:
            f.write(str(i))

        sender = potential['sender']
        url = potential['url']
        
        try:
            song = Song(url, None, sender=sender)
        except:
            with_error += 1
            with open('with_error.txt', 'a') as f:
                f.write(f'{url}\n')

        if song.is_good:
            if similar(song.display_name(), song.yt_name) > MINIMUM_SIMILARITY:
                songs += 1
                with open('extracted.txt', 'a') as f:
                    f.write(f'{song}\n')
                with open('extracted.csv', 'a') as f:
                    f.write(f'{song.short()}\n')
            else:
                not_similar += 1
                with open('not_similar.txt', 'a') as f:
                    f.write(f'{song}\n')
        else:
            with_error += 1
            with open('with_error.txt', 'a') as f:
                f.write(f'{url}\n')

    print(f'Number of potentials: {num_of_potentials}\n')
    print(f'Total songs extracted: {songs}')
    print(f'Extract errors: {with_error}')
    print(f'Not similar: {not_similar}')


if __name__ == '__main__':
    start_time = datetime.now()
    print('-------------------- START --------------------\n')
    main()
    print('\n--------------------  END  --------------------')
    end_time = datetime.now()

    delta = end_time - start_time
    print(f'\nTime taken: {str(delta)}')
