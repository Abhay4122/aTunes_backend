from fastapi import APIRouter, Depends, status
from config import get_db
from sqlalchemy import or_
from sqlalchemy.orm import Session
import models, json, utils, schemas, time, requests


router = APIRouter(prefix='/f-test', tags=['Test data'])

@router.get('')
def get_songs():
  """
    Return the List of universities for some random countries in sync way
  """
  hel
  data: dict = {}
  data.update(get_all_universities_for_country("turkey"))
  data.update(get_all_universities_for_country("india"))
  data.update(get_all_universities_for_country("australia"))
  return data


def get_all_universities_for_country(country: str) -> dict:
    
    url = 'http://universities.hipolabs.com/search'
    params = {'country': country}
    response = requests.get(url, params=params)
    response_json = json.loads(response.text)
    universities = []
    for university in response_json:
        # university_obj = University.parse_obj(university)
        universities.append(university)
    return {country: universities}