from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class VideoBase(BaseModel):
    title: str
    url: str
    video_id: str
    description: str
    upload_date: datetime

class VideoCreate(VideoBase):
    channel_id: int

class Video(VideoBase):
    id: int
    channel_id: int
    created_at: datetime
    channel_name: str  # Add this field

    class Config:
        orm_mode = True
        from_attributes = True

class ChannelBase(BaseModel):
    name: str
    channel_id: str

class ChannelCreate(ChannelBase):
    pass

class Channel(ChannelBase):
    id: int
    created_at: datetime
    videos: List[Video] = []

    class Config:
        orm_mode = True
