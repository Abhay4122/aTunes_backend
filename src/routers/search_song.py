from fastapi import APIRouter, Depends, status
from config import get_db
from sqlalchemy import or_
from sqlalchemy.orm import Session
import models, json, utils, schemas


router = APIRouter(prefix='/search-song', tags=['Songs data'])

@router.get('')
def get_songs(_serch: str = '', db: Session = Depends(get_db)):
  '''
    URL (/search-song) is used to seasrch the songs song name, year, artist, gener, movie
  '''
  modl = models.SongDetails

  songs_data = []

  if _serch:
    songs_data = db.query(modl).filter(or_(modl.title.ilike(f'%{_serch}%'), modl.movie_name.ilike(f'%{_serch}%'))).all()
  else:
    {'msg': 'Sorry, no data found!'}

  return utils.resp_format(songs_data, status.HTTP_200_OK, schemas.GetSongsList)
