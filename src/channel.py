import json
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import isodate
from settings import NAME_DIR


class Channel:
    """Класс для ютуб-канала"""
    load_dotenv(NAME_DIR)
    api_key: str = os.getenv('YT_API_KEY')
    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)
    list_ = []

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        channel = Channel.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.__channel_id = channel
        self.id = channel_id
        item = channel['items'][0]
        self.__title = item['snippet']['title']
        self.__video_count = item['statistics']['videoCount']
        self.description = item['snippet']['description']
        self.view_count = item['statistics']['viewCount']
        self.subscriber = int(item['statistics']['subscriberCount'])
        kind = item['kind'].split('#')
        self.__url = f'https://www.{kind[0]}.com/{kind[1]}/{self.id}'

    def __str__(self):
        return f"{self.__title}\n{self.__url}"

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
        return self.__title

    @property
    def video_count(self):
        return self.__video_count

    @property
    def url(self):
        return self.__url

    @classmethod
    def get_service(cls):
        """
        возвращающий объект для работы с YouTube API
        """
        return cls.youtube

    def to_json(self, file_name: str) -> None:
        """
        сохраняющий в файл значения атрибутов экземпляра Channel
        """
        data = json.dumps(self.__channel_id)
        with open(file_name, 'a', encoding='utf-8') as file:
            file.write(data)


if __name__ == '__main__':
    c1 = Channel('UC-OVMPlMA3-YCIeg4z5z23A')
    c = Channel('UCwHL6WHUarjGfUM_586me8w')
    c1.print_info()
    # https://www.youtube.com/channel/UC-OVMPlMA3-YCIeg4z5z23A

