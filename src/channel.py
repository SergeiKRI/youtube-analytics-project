import json
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
from settings import NAME_DIR


class Channel:
    """Класс для ютуб-канала"""
    load_dotenv(NAME_DIR)
    api_key: str = os.getenv('YT_API_KEY')
    # создать специальный объект для работы с API
    __youtube = build('youtube', 'v3', developerKey=api_key)
    list_ = []

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        channel = Channel.__youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.__channel_id = channel
        self.id = channel_id
        self.item = channel['items'][0]

    def __str__(self) -> str:
        return f"{self.title}\n{self.url}"

    def __add__(self, other) -> int:
        return self.subscriber + other.subscriber

    def __sub__(self, other) -> int:
        return self.subscriber - other.subscriber

    def __gt__(self, other) -> bool:
        return self.subscriber > other.subscriber

    def __ge__(self, other) -> bool:
        return self.subscriber >= other.subscriber

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.__channel_id, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.item['snippet']['title']

    @property
    def video_count(self):
        return self.item['statistics']['videoCount']

    @property
    def url(self):
        kind = self.item['kind'].split('#')
        url = f'https://www.{kind[0]}.com/{kind[1]}/{self.id}'
        return url

    @property
    def description(self):
        return self.item['snippet']['description']

    @property
    def view_count(self):
        return self.item['statistics']['viewCount']

    @property
    def subscriber(self):
        return int(self.item['statistics']['subscriberCount'])

    @classmethod
    def get_service(cls):
        """
        возвращающий объект для работы с YouTube API
        """
        return cls.__youtube

    def to_json(self, file_name: str) -> None:
        """
        сохраняющий в файл значения атрибутов экземпляра Channel
        """
        data = json.dumps(self.__channel_id)
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(data)


if __name__ == '__main__':
    c1 = Channel('UC-OVMPlMA3-YCIeg4z5z23A')
    c = Channel('UCwHL6WHUarjGfUM_586me8w')
    c1.print_info()
    # https://www.youtube.com/channel/UC-OVMPlMA3-YCIeg4z5z23A

