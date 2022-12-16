from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import songs_data
from config import cursor, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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
  query = '''
      select * from song_details;
  '''

  print('Hello')

  data = cursor(query)
  
  return data


app.include_router(songs_data.router)
