from .message import Message


class LinkFinder:

    def __init__(self, supported_domains: list[str]) -> None:
        self.supported_domains = supported_domains

    def get_urls(self, messages: list[Message], excluded_senders: list[str] = None) -> list[dict[str, str]]:
        potentials: list[dict[str, str]] = []

        for message in messages:
            if excluded_senders and message.sender in excluded_senders:
                continue

            for word in message.content.split():
                if any(word.startswith(domain) for domain in self.supported_domains):
                    potentials.append({
                        'sender': message.sender,
                        'url': word.strip(' <>"#%{}|\\^~[]`)'),
                    })

        return potentials
