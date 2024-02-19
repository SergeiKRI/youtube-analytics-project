import datetime
from datetime import timedelta
import os

import isodate
from googleapiclient.discovery import build
from dotenv import load_dotenv
from settings import NAME_DIR


class PlayList:
    """инициализируется id плейлиста по API"""
    load_dotenv(NAME_DIR)
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, play_list_id):
        self.play_list = play_list_id
        self.playlist_response = PlayList.get_serves().playlists().list(id=play_list_id,
                                                                        part='contentDetails, snippet',
                                                                        maxResults=50,
                                                                        ).execute()
        self.playlist_videos = PlayList.get_serves().playlistItems().list(playlistId=play_list_id,
                                                                          part='contentDetails',
                                                                          maxResults=50,
                                                                          ).execute()

        self.video_response = PlayList.get_serves().videos().list(part='contentDetails,statistics',
                                                                  id=','.join(
                                                                      [video['contentDetails']['videoId'] for video in
                                                                       self.playlist_videos['items']])
                                                                  ).execute()

    @property
    def url(self) -> str:
        return "https://www.youtube.com/playlist?list=" + self.play_list

    @property
    def title(self) -> str:
        return self.playlist_response['items'][0]['snippet']['title']

    @property
    def total_duration(self) -> timedelta:
        """возвращает объект класса с суммарной длительность плейлиста"""

        total_duration = datetime.timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += datetime.timedelta(seconds=duration.total_seconds())
        return total_duration

    def show_best_video(self) -> str:
        """возвращает ссылку на самое популярное видео из плейлиста"""

        max_like = 0
        max_video = ""
        for video in self.video_response['items']:
            count_like = video['statistics']['likeCount']
            count_video = video['id']
            if int(count_like) > int(max_like):
                max_video = count_video

        return f"https://youtu.be/{max_video}"

    @classmethod
    def get_serves(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)
