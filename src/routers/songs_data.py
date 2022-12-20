from fastapi import APIRouter, Depends, status
from config import get_db
from sqlalchemy.orm import Session
import models, json, utils, schemas


router = APIRouter(prefix='/songs-data', tags=['Songs data'])

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
  from pathlib import Path
  
  BASE_DIR = Path(__file__).resolve().parent.parent
  file_path = str(BASE_DIR) + '/raw_data/data.json'

  f = open(file_path, 'r')
  raw_data = json.loads(f.read())

  for char in raw_data:
    for movie in char['children']:
      for song in movie['children']:
        try:
          song_data = modl(**{
            'movie_name': song.get('Movie / Album', ''), 'title': song.get('title', ''),
            'year': song.get('Year', ''), 'tag_line': song.get('Tagline', ''),
            'release_date': song.get('Release Date', ''), 'cast': song.get('Cast', ''),
            'director': song.get('Director', ''), 'genre': song.get('Genre', ''),
            'rating': song.get('Rating', ''), 'writer': song.get('Writer', ''),
            'movie_folder': movie.get('title', '')
          })

          db.add(song_data)
          db.commit()
          db.refresh(song_data)
        except Exception as e:
          print(e)