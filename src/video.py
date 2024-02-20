import os
from pprint import pprint

from googleapiclient.discovery import build
from dotenv import load_dotenv
from settings import NAME_DIR


class Video:
    """Класс для информации о видео с Youtube"""
    load_dotenv(NAME_DIR)
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, video_id):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id
        self.video_response = Video.get_serves().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                   id=video_id
                                                                   ).execute()
        if len(self.video_response['items']) == 0:
            self.video_id = None

    def __str__(self):
        if self.title is None:
            return ''
        return self.title

    @property
    def url_video(self):
        if self.video_id is None:
            return None
        return "https://youtu.be/" + self.video_id

    @property
    def title(self):
        if self.video_id is None:
            return None
        return self.video_response['items'][0]['snippet']['title']

    @property
    def view_count(self):
        if self.video_id is None:
            return None
        return self.video_response['items'][0]['statistics']['viewCount']

    @property
    def like_count(self) -> int:
        if self.video_id is None:
            return None
        return self.video_response['items'][0]['statistics']['likeCount']

    @classmethod
    def get_serves(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)


class PLVideo(Video):
    """Класс для 'id видео' и 'id плейлиста'"""

    def __init__(self, video_id, playlist_id):
        self.video_id = video_id
        super().__init__(video_id)
        self.playlist_videos = Video.get_serves().playlistItems().list(playlistId=playlist_id,
                                                                       part='contentDetails',
                                                                       maxResults=50,
                                                                       ).execute()

    @property
    def video_ids(self):
        return [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]


if __name__ == '__main__':
    video2 = PLVideo('4fObz_qw9u4', 'PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC')
    print(video2.video_ids)
