import json
import os
from googleapiclient.discovery import build

import isodate

class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        channel = Channel.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.channel_id = channel

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel_id, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    c = Channel('UC-OVMPlMA3-YCIeg4z5z23A')
    c.print_info()
