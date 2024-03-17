def get_urls(filename: str, excluded: list[str] = None) -> list[dict]:

    with open(filename, 'r') as backup:
        raw: str = backup.read()


    messages: list[str] = raw.split('\n')

    yt_domains = ['https://youtube.com', 'https://m.youtube.com', 'https://youtu.be']


    potential_reccomendations: list[dict] = []

    for message in messages:
        potential = {}
        try:
            sender = message.split(':')[1][5:]
        except:
            continue

        if excluded is not None and sender in excluded:
            continue
        potential['sender'] = sender

        words = message.split()
        for domain in yt_domains:
            if domain in message:
                for word in words:
                    if domain in word:
                        potential['url'] = word
                        potential_reccomendations.append(potential)

    return potential_reccomendations
