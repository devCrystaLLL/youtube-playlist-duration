import re
from datetime import timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from util.Playlist import Playlist
from util.Duration import Duration
import util.Duration as duration


class YtPlaylistDuration:
    PLAYLIST_NOT_VALID_ERROR = ""

    api_key = ""
    youtube = None

    hours_pattern = None
    minutes_pattern = None
    seconds_pattern = None

    total_seconds = 0
    nextPageToken = None

    def __init__(self, apiKey):
        global PLAYLIST_NOT_VALID_ERROR, api_key, youtube, hours_pattern, minutes_pattern, seconds_pattern, total_seconds, nextPageToken

        PLAYLIST_NOT_VALID_ERROR = "error_playlist_url_not_valid"

        api_key = apiKey
        youtube = build('youtube', 'v3', developerKey=api_key)

        hours_pattern = re.compile(r'(\d+)H')
        minutes_pattern = re.compile(r'(\d+)M')
        seconds_pattern = re.compile(r'(\d+)S')

        total_seconds = 0

        nextPageToken = None

    def get_playlist_by_url(self, playlist_link: str):
        playlist_id = self.get_playlist_id_from_url(self, playlist_link)
        return self.get_playlist_by_id(self, playlist_id)

    def get_playlist_id_from_url(self, playlist_link: str):
        playlist_url_split = playlist_link.split('list=')

        if len(playlist_url_split) > 1:
            return playlist_url_split[1]
        else:
            return PLAYLIST_NOT_VALID_ERROR

    def get_playlist_by_id(self, playlist_id: str):
        global api_key, youtube, hours_pattern, minutes_pattern, seconds_pattern, total_seconds, nextPageToken

        video_duration = Duration()
        average_video_duration = Duration()
        playlist = Playlist(playlist_id, video_duration, average_video_duration)

        while True:
            pl_request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=nextPageToken
            )

            try:
                pl_response = pl_request.execute()
            except HttpError:
                playlist.isValid = False
                return playlist

            playlist.number_of_videos = pl_response['pageInfo']['totalResults']

            vid_ids = []
            for video in pl_response['items']:
                vid_ids.append(video['contentDetails']['videoId'])

            vid_request = youtube.videos().list(
                part="contentDetails",
                id=','.join(vid_ids)
            )

            vid_response = vid_request.execute()

            for video in vid_response['items']:
                video_duration = video['contentDetails']['duration']

                hours = hours_pattern.search(video_duration)
                minutes = minutes_pattern.search(video_duration)
                seconds = seconds_pattern.search(video_duration)

                hours = int(hours.group(1)) if hours else 0
                minutes = int(minutes.group(1)) if minutes else 0
                seconds = int(seconds.group(1)) if seconds else 0

                video_seconds = timedelta(
                    hours=hours,
                    minutes=minutes,
                    seconds=seconds
                ).total_seconds()

                total_seconds += video_seconds

            nextPageToken = pl_response.get('nextPageToken')

            if not nextPageToken:
                break

        total_seconds = int(total_seconds)
        playlist.playlist_duration.total_seconds = total_seconds
        average_length_of_video_in_secs = total_seconds / playlist.number_of_videos

        playlist.average_video_duration = duration.convert_from_seconds_to_duration(average_length_of_video_in_secs)
        playlist.playlist_duration = duration.convert_from_seconds_to_duration(total_seconds)

        return playlist
