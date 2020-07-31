from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

Base = declarative_base()
Engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=Engine)


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String)


Base.metadata.create_all(Engine)
