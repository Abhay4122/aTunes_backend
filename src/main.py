from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import songs_data, play_song, search_song, f_test
from config import cursor, engine
import models, time

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


@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
    return response


@app.get('/')
def index():
  # query = '''
  #     select * from song_details;
  # '''

  # data = cursor(query)
  data = {'Hello': 'World'}
  
  return data

app.include_router(songs_data.router)
app.include_router(play_song.router)
app.include_router(search_song.router)
app.include_router(f_test.router)
