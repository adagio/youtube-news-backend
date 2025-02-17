import os
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from collections import deque

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class YouTubeClient:
    def __init__(self):
        self.youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
        self.rate_limit = deque(maxlen=100)
    
    def _rate_limit(self):
        while len(self.rate_limit) == 100 and time.time() - self.rate_limit[0] < 100:
            time.sleep(1)
        self.rate_limit.append(time.time())

    def get_channel_id_from_handle(self, handle: str) -> str:
        """Convert a YouTube handle (e.g. @channelname) to channel ID"""
        self._rate_limit()
        try:
            # Remove @ if present
            handle = handle.lstrip('@')
            response = self.youtube.search().list(
                q=f"@{handle}",
                type='channel',
                part='id',
                maxResults=1
            ).execute()
            
            items = response.get('items', [])
            if items:
                return items[0]['id']['channelId']
            return None
        except HttpError as e:
            if e.resp.status in [403, 500, 503]:
                time.sleep(5)
                return self.get_channel_id_from_handle(handle)
            else:
                raise e

    def get_latest_videos(self, channel_id: str, max_results=10):
        self._rate_limit()
        try:
            response = self.youtube.search().list(
                channelId=channel_id,
                part="snippet",
                order="date",
                type="video",  # Add type parameter to only get videos
                maxResults=max_results
            ).execute()
            
            # Filter out any remaining non-video items
            items = response.get("items", [])
            videos = [
                item for item in items 
                if item.get("id", {}).get("kind") == "youtube#video"
            ]
            
            return videos
        except HttpError as e:
            if e.resp.status in [403, 500, 503]:
                time.sleep(5)
                return self.get_latest_videos(channel_id, max_results)
            else:
                raise e
            
    def get_video_details(self, video_id: str):
        self._rate_limit()
        try:
            response = self.youtube.videos().list(
                part="snippet",
                id=video_id
            ).execute()
            return response.get("items", [])
        except HttpError as e:
            if e.resp.status in [403, 500, 503]:
                time.sleep(5)
                return self.get_video_details(video_id)
            else:
                raise e
