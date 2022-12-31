from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import songs_data, play_song, search_song
from config import cursor, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(redoc_url=None)

origins = ['*']
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*']
)

@app.get('/')
def index():
  # query = '''
  #     select * from song_details;
  # '''

  # data = cursor(query)
  data = {}
  
  return data


app.include_router(songs_data.router)
app.include_router(play_song.router)
app.include_router(search_song.router)
