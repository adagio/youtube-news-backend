from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database
from typing import List

router = APIRouter(
    prefix="/channels",
    tags=["channels"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.Channel])
def read_channels(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    channels = db.query(models.Channel).offset(skip).limit(limit).all()
    return channels

@router.post("/", response_model=schemas.Channel)
def create_channel(channel: schemas.ChannelCreate, db: Session = Depends(get_db)):
    db_channel = db.query(models.Channel).filter(models.Channel.channel_id == channel.channel_id).first()
    if db_channel:
        raise HTTPException(status_code=400, detail="Channel already registered")
    new_channel = models.Channel(**channel.dict())
    db.add(new_channel)
    db.commit()
    db.refresh(new_channel)
    return new_channel

@router.delete("/{channel_id}", response_model=schemas.Channel)
def delete_channel(channel_id: int, db: Session = Depends(get_db)):
    channel = db.query(models.Channel).filter(models.Channel.id == channel_id).first()
    if channel is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    db.delete(channel)
    db.commit()
    return channel
