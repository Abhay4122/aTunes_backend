from fastapi import APIRouter

router = APIRouter(prefix='/songs-data', tags='Songs data')

@router.get('')
def get_songs():
  '''
    URL (/songs_data) is used to  get the songs with filter by name, year, artist, gener
  '''

  return {'data': 'All songs'}