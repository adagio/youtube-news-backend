from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import models, schemas, database

router = APIRouter(
    prefix="/videos",
    tags=["videos"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.Video])
def read_videos(
    title: Optional[str] = None,
    channel_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(
        models.Video,
        models.Channel.name.label('channel_name')
    ).join(models.Channel).order_by(models.Video.upload_date.desc())
    
    if title:
        query = query.filter(models.Video.title.contains(title))
    if channel_id:
        query = query.filter(models.Video.channel_id == channel_id)
    
    results = query.offset(skip).limit(limit).all()
    
    # Convert results to list of Video objects with channel name
    videos = []
    for video, channel_name in results:
        video_dict = {
            **video.__dict__,
            'channel_name': channel_name
        }
        videos.append(video_dict)
    
    return videos
