from fastapi import APIRouter, Depends, status
from config import get_db, redis_search
from sqlalchemy import or_
from sqlalchemy.orm import Session
import models, json, utils, schemas, os
from pathlib import Path


router = APIRouter(prefix='/songs-data', tags=['Songs data'])

@router.get('')
def get_songs(_all: str = '', _id: str = '', _page: str = '', _serch: str = '', db: Session = Depends(get_db)):
  '''
    URL (/songs-data) is used to get the songs with filter by name, year, artist, gener
  '''
  modl = models.SongDetails

  songs_data = []

  if _all:
    songs_data = db.query(modl).order_by(modl.title.desc()).all()
  elif _page:
    songs_data = db.query(modl).order_by(modl.title.desc()).limit(10).offset(int(_page)-1).all()
  elif _id:
    songs_data = db.query(modl).filter(modl.id == _id).all()
  elif _serch:
    if _serch == 'data_fill_kro':
      sync_with_db(db, modl)
    else:
      songs_data = db.query(modl).filter(or_(modl.title.ilike(f'%{_serch}%'), modl.movie_name.ilike(f'%{_serch}%'))).all()
  else:
    songs_data = db.query(modl).order_by(modl.title.desc()).limit(20).all()

  return utils.resp_format(songs_data, status.HTTP_200_OK, schemas.GetSongsList)

def sync_with_db(db, modl):
  base_dir = Path(__file__).resolve().parent.parent
  files_list = os.listdir(str(base_dir) + '/raw_data')

  for file in files_list:
    file_path = f'{str(base_dir)}/raw_data/{file}'
    
    f = open(file_path, 'r')
    raw_data = json.loads(f.read())
    category = file.split('.')[0]
    r_con = redis_search()

    for char in raw_data:
      for movie in char['children']:
        for song in movie['children']:
          savable_data = {
            'movie_name': song.get('Movie / Album', ''), 'title': song.get('title', ''),
            'year': song.get('Year', ''), 'tag_line': song.get('Tagline', ''),
            'release_date': song.get('Release Date', ''), 'cast': song.get('Cast', ''),
            'director': song.get('Director', ''), 'genre': song.get('Genre', ''),
            'rating': song.get('Rating', ''), 'writer': song.get('Writer', ''),
            'movie_folder': movie.get('title', ''), 'movie_img': song.get('img', '').split('/')[-1],
            'category_name': category, 'movie_name_year': song.get('Name', '')
          }

          try:
            _song = db.query(modl).filter(
                modl.title == song.get('title', ''), modl.movie_name_year == song.get('Name', ''), modl.year == song.get('Year', '')
            ).all()

            if not _song:
              song_data = modl(**savable_data)

              db.add(song_data)
              db.commit()
              db.refresh(song_data)

              sync_with_redis(r_con, category, savable_data)
            else:
              print(f"{song.get('title', '')} not saved.")

          except Exception as e:
            print(e)
  
def sync_with_redis(client, category, data):
  client.redis.hset(
    f'all_song:{category}_{data["title"]}',
    mapping={
      'title': data['title'],
      'body': json.dumps({'movie_name': data['movie_name'], 'title': data['title']})
    }
  )
