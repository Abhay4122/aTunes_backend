from fastapi import APIRouter, Depends, status
from config import get_db, redis_search
from sqlalchemy import or_
from sqlalchemy.orm import Session
import models, json, utils, schemas


router = APIRouter(prefix='/search-song', tags=['Search songs'])

@router.get('')
def get_songs(_serch: str = '', db: Session = Depends(get_db)):
  '''
    URL (/search-song) is used to seasrch the songs song name, year, artist, gener, movie
  '''
  modl = models.SongDetails
  r_con = redis_search()

  songs_data = []

  if _serch:
    # songs_data = db.query(modl).filter(or_(modl.title.ilike(f'%{_serch}%'), modl.movie_name.ilike(f'%{_serch}%'))).all()
    raw_search = r_con.search(f'@title:{_serch}')

    for i in raw_search.docs:
      songs_data.append(json.loads(i.body))
  else:
    {'msg': 'Sorry, no data found!'}

  return utils.resp_format(songs_data, status.HTTP_200_OK)
