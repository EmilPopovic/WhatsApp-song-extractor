from datetime import datetime


class Message:
    __DATE_SENDER_SEPARATOR = ' - '
    __SENDER_CONTENT_SEPARATOR = ': '
    __DATE_FORMAT = '%m/%d/%y, %H:%M'
    __ATTACHMENT_FLAG = ' (file attached)\n'
    __MEDIA_OMITTED_FLAG = '<Media omitted>\n'
    __EDITED_MESSAGE_FLAG = '<This message was edited>\n'

    def __init__(self,
                 content: str,
                 sender: str,
                 timestamp: datetime,
                 file_attached: str | None = None,
                 edited: bool = False,
                 media_omitted: bool = False) -> None:
        self.file_attached = file_attached
        self.timestamp = timestamp
        self.sender = sender
        self.content = content
        self.file_attached = file_attached
        self.edited = edited
        self.media_omitted = media_omitted

    @classmethod
    def __create_message_with_flags(cls,
                                    content: str,
                                    sender: str,
                                    timestamp: datetime,
                                    file_attached: str) -> 'Message':
        media_omitted = False
        if content == cls.__MEDIA_OMITTED_FLAG:
            content = content.replace(cls.__MEDIA_OMITTED_FLAG, '')
            media_omitted = True

        edited = False
        if content.endswith(cls.__EDITED_MESSAGE_FLAG):
            content = content.replace(cls.__EDITED_MESSAGE_FLAG, '\n')
            edited = True

        return Message(content, sender, timestamp, file_attached, edited, media_omitted)

    @classmethod
    def parse_txt(cls, path: str) -> list['Message']:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        messages: list[Message] = []

        content: str | None = None
        sender: str | None = None
        timestamp: datetime | None = None
        file_attached: str | None = None

        for line in lines:

            # this is probably the message head
            if cls.__DATE_SENDER_SEPARATOR in line and cls.__SENDER_CONTENT_SEPARATOR in line:
                if content is not None:
                    messages.append(cls.__create_message_with_flags(content, sender, timestamp, file_attached))

                    content = None
                    sender = None
                    timestamp = None
                    file_attached = None

                split_by_date_sep = line.split(cls.__DATE_SENDER_SEPARATOR)

                timestamp_str = split_by_date_sep[0]

                try:
                    timestamp = datetime.strptime(timestamp_str, cls.__DATE_FORMAT)
                except ValueError as _:
                    # this is in fact not the message head
                    pass
                else:
                    # this is the message head
                    split_by_sender_sep = (cls.__DATE_SENDER_SEPARATOR
                                           .join(split_by_date_sep[1:])
                                           .split(cls.__SENDER_CONTENT_SEPARATOR))

                    sender = split_by_sender_sep[0]
                    content = (cls.__SENDER_CONTENT_SEPARATOR
                               .join(split_by_sender_sep[1:]))

                    if content.endswith(cls.__ATTACHMENT_FLAG):
                        file_attached = content[:-len(cls.__ATTACHMENT_FLAG)]
                        content = ''

                    continue

            # this is not the message head
            if content:
                content += line
            else:
                content = line

        messages.append(cls.__create_message_with_flags(content, sender, timestamp, file_attached))

        return messages

    def __repr__(self) -> str:
        return (f'{self.timestamp} - {self.sender}'
                f'{f'\n<Edited>' if self.edited else ''}'
                f'{f'\n<Media omitted>' if self.media_omitted else ''}'
                f'{f'\n<Attachment: {self.file_attached}>' if self.file_attached else ''}'
                f'\n{self.content}')


if __name__ == '__main__':
    parsed_messages = Message.parse_txt('../../data/backup_large.txt')
    for message in parsed_messages:
        print(message)
