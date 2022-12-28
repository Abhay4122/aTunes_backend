from fastapi import APIRouter, Depends, status
from config import get_db
from sqlalchemy.orm import Session
from pathlib import Path
from os import environ
import models, json, utils, schemas, boto3


S3_CLIENT = boto3.client(
    's3', aws_access_key_id = environ.get('ACCESS_KEY'),
    aws_secret_access_key = environ.get('SECRET_KEY'),
    region_name = environ.get('REGION')
)

router = APIRouter(prefix='/play-song', tags=['Play song'])

@router.get('')
def get_songs(_id: str = '', db: Session = Depends(get_db)):
    '''
        URL (/play-song) is used to Play the song ondemand
    '''
    modl = models.SongDetails
    songs_data = db.query(modl).filter(modl.id == _id).first()

    obj = S3_CLIENT.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': environ.get('BUCKET'),
            'Key': f'songs/{"".join(e for e in songs_data.movie_folder if e.isalnum())}/{songs_data.title}.mp3'
        },
        ExpiresIn=600
    )
    
    return utils.resp_format(obj, status.HTTP_200_OK)