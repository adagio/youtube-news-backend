from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Channel
from youtube_client import YouTubeClient

Base.metadata.create_all(bind=engine)

def preload_channels():
    db: Session = SessionLocal()
    youtube_client = YouTubeClient()

    channels = [
        {"name": "Cosas Militares", "channel_handle": "@CosasMilitares"},
        {"name": "Monitor Fantasma", "channel_handle": "@Monitorfantasma"},
        {"name": "Oscar Vara", "channel_handle": "@oscarvara"},
        {"name": "Marc Vidal", "channel_handle": "@marc_vidal"},
        {"name": "Alex Fidalgo", "channel_handle": "@Loquetudigas"},
        {"name": "Cascarón de Nuez", "channel_handle": "@jfcalero"},
        {"name": "Gustavo Entrala", "channel_handle": "@@gustavo-entrala"},
        {"name": "Noticias Ilustradas", "channel_handle": "@NOTICIASILUSTRADAS"},
        {"name": "Dudas eternas", "channel_handle": "@DudasEternas"},
        {"name": "midulive", "channel_handle": "@midulive"},
        {"name": "midudev", "channel_handle": "@midudev"},
        {"name": "MoureDev TV", "channel_handle": "@mouredevtv"},
        {"name": "MoureDev", "channel_handle": "@mouredev"}
    ]
    for channel in channels:
        channel_id = youtube_client.get_channel_id_from_handle(channel["channel_handle"])
        if channel_id:
            db_channel = db.query(Channel).filter(Channel.channel_id == channel_id).first()
            if not db_channel:
                new_channel = Channel(name=channel["name"], channel_id=channel_id)
                db.add(new_channel)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    preload_channels()
