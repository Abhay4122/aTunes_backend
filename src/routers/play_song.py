from fastapi import APIRouter, Depends, status
from config import get_db
from sqlalchemy.orm import Session
from pathlib import Path
import models, json, utils, schemas


router = APIRouter(prefix='/play-song', tags=['Play song'])

@router.get('')
def get_songs(_id: str = '', db: Session = Depends(get_db)):
    '''
        URL (/play-song) is used to Play the song ondemand
    '''

    modl = models.SongDetails

    songs_data = db.query(modl).filter(modl.id == _id).first()
    
    return utils.resp_format(songs_data, status.HTTP_200_OK, schemas.GetSongsList)