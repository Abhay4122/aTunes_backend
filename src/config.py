import boto3, psycopg2, time, os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from redisearch import Client, TextField, IndexDefinition


HOST = 'db'
USER = os.environ.get('POSTGRES_USER')
PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB = os.environ.get('POSTGRES_DB')


def get_s3_client():
    conn = boto3.resource(
        's3', aws_access_key_id = os.environ.get('ACCESS_KEY'),
        aws_secret_access_key = os.environ.get('SECRET_KEY'),
        region_name = os.environ.get('REGION')
    )

    return 'bucket'

engine = create_engine(f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}/{DB}')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def cursor(query):
    con = psycopg2.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB
    )

    cursor = con.cursor()

    try:
        cursor.execute(query)

        return cursor.fetchall()
    except Exception as e:
        print('Connection to dtabase is failed.')
        print(f'Error: {e}')
        time.sleep(10)
    finally:
        cursor.close()

def redis_search():
    # Creating a client with a given index name
    client = Client('index-document', host='search')

    # IndexDefinition is available for RediSearch 2.0+
    definition = IndexDefinition(prefix=f'all_song:')

    # Creating the index definition and schema
    try:
      client.create_index(
        (TextField('title'), TextField('body')),
        definition=definition              
      )
    except Exception as e:
      pass

    return client