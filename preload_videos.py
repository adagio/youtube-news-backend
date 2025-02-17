from sqlalchemy.orm import Session
from database import SessionLocal
from models import Channel, Video
from youtube_client import YouTubeClient
from datetime import datetime

def fetch_latest_videos():
    db: Session = SessionLocal()
    youtube_client = YouTubeClient()

    # Get all channels from database
    channels = db.query(Channel).all()
    
    for channel in channels:
        videos = youtube_client.get_latest_videos(channel.channel_id)
        for video in videos:
            try:
                video_id = video['id']['videoId']
                # Check if video already exists
                exists = db.query(Video).filter(Video.video_id == video_id).first()
                if not exists:                    
                    new_video = Video(
                        title=video['snippet']['title'],
                        description=video['snippet']['description'],
                        video_id=video_id,
                        url=f"https://www.youtube.com/watch?v={video_id}",
                        upload_date=datetime.fromisoformat(video['snippet']['publishedAt'].replace('Z', '+00:00')),
                        channel_id=channel.id,
                    )
                    db.add(new_video)
            except KeyError:
                print(f"KeyError: 'videoId' not found in video data: {video}")
                print(f"channel is: {channel}")
    
    db.commit()
    db.close()

if __name__ == "__main__":
    fetch_latest_videos()