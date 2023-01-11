from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class GetSongsList(BaseModel):
    id: UUID
    title: str
    category_name: Optional[str] = None
    movie_name: Optional[str] = None
    movie_img: Optional[str] = None
    year: Optional[str] = None
    tag_line: Optional[str] = None
    release_date: Optional[str] = None
    cast: Optional[str] = None
    title: Optional[str] = None
    director: Optional[str] = None
    genre: Optional[str] = None
    rating: Optional[str] = None
    writer: Optional[str] = None
    movie_folder: Optional[str] = None
    movie_name_year: Optional[str] = None

    class Config:
        orm_mode = True
