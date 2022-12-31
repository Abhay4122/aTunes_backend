import uuid
from config import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects import postgresql


class SongDetails(Base):
    __tablename__ = 'song_details'

    id = Column(postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True
    )
    movie_name = Column(String(200), nullable=False)
    movie_img = Column(String(250), nullable=False)
    title = Column(String(200), nullable=False)
    year = Column(String(5), nullable=True)
    tag_line = Column(String(250), nullable=True)
    release_date = Column(String(50), nullable=True)
    cast = Column(String(200), nullable=True)
    director = Column(String(100), nullable=True)
    genre = Column(String(100), nullable=True)
    rating = Column(String(15), nullable=True)
    writer = Column(String(100), nullable=True)
    movie_folder= Column(String(200), nullable=True)