
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE= "mysql+pymysql://root@localhost:3306/vision_vantage"

engine = create_engine(URL_DATABASE, echo=True)  # `echo=True` helps with debugging
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()