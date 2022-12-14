import boto
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_s3_client():
    conn = boto.connect_s3('AKIARUYJYFCS6I7UCPMD', '4rnhTe7GalZABQrrxj001rMcypffVcl8E/ieIGNJ')
    bucket = conn.get_bucket('gpsurvey')

    return bucket

engine = create_engine('postgresql+psycopg2://ssh_script:Zxcvbnmm032241@django.db.backends.postgresql_psycopg2/db_office')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()