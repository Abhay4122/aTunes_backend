from config import Base
from sqlalchemy import Column, Integer, String, DateTime


class SongDetails(Base):
    __tablename__ = 'song_details'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(200), nullable=False)
    path = Column(String(200), nullable=False)