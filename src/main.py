from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import songs_data

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
  return {'Name': 'Abhay singh'}


app.include_router(songs_data.router)
