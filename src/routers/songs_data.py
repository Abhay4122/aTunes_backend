from fastapi import APIRouter, Depends
from config import get_db
from sqlalchemy.orm import Session
from pathlib import Path
import models, json


router = APIRouter(prefix='/songs-data', tags=['Songs data'])

BASE_DIR = Path(__file__).resolve().parent.parent

@router.get('')
def get_songs(db: Session = Depends(get_db)):
  '''
    URL (/songs-data) is used to get the songs with filter by name, year, artist, gener
  '''
  # file_path = str(BASE_DIR) + '/raw_data/data.json'

  # f = open(file_path, 'r')
  # raw_data = json.loads(f.read())

  # for char in raw_data:
  #   for movie in char['children']:
  #     for song in movie['children']:
  #       song_data = models.SongDetails(**{'movie_name': movie['title'], 'title': song['title']})

  #       db.add(song_data)
  #       db.commit()
  #       db.refresh(song_data)

  return {'data': 'All songs'}