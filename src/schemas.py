from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class GetSongsList(BaseModel):
    id: UUID
    title: str
    movie_name: Optional[str] = None

    class Config:
        orm_mode = True
