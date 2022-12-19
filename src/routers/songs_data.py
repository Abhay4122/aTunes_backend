from fastapi import APIRouter, Depends, status
from config import get_db
from sqlalchemy.orm import Session
from pathlib import Path
import models, json, utils, schemas


router = APIRouter(prefix='/songs-data', tags=['Songs data'])

BASE_DIR = Path(__file__).resolve().parent.parent

@router.get('')
def get_songs(_all: str = '', _id: str = '', _page: str = '', db: Session = Depends(get_db)):
  '''
    URL (/songs-data) is used to get the songs with filter by name, year, artist, gener
  '''
  modl = models.SongDetails
  
  # sync_with_db(db, modl)

  songs_data = []

  if _all:
    songs_data = db.query(modl).order_by(modl.title.desc()).all()
  elif _page:
    songs_data = db.query(modl).order_by(modl.title.desc()).limit(10).offset(int(_page)-1).all()
  elif _id:
    songs_data = db.query(modl).filter(modl.id == _id).all()
  else:
    songs_data = db.query(modl).order_by(modl.title.desc()).limit(20).all()

  return utils.resp_format(songs_data, status.HTTP_200_OK, schemas.GetSongsList)

def sync_with_db(db, modl):
  file_path = str(BASE_DIR) + '/raw_data/data.json'

  f = open(file_path, 'r')
  raw_data = json.loads(f.read())

  for char in raw_data:
    for movie in char['children']:
      for song in movie['children']:
        song_data = modl(**{'movie_name': movie['title'], 'title': song['title']})

        db.add(song_data)
        db.commit()
        db.refresh(song_data)