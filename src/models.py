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
    title = Column(String(200), nullable=False)