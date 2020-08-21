import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

Base = declarative_base()
Engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=Engine)


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<Article(id='%s', title='%s', url='%s')>" % (self.id, self.title, self.url)

    def save(self):
        session = Session()
        session.add(self)
        session.commit()

    @classmethod
    def create(cls, *, title, url):
        article = cls()
        article.title = title
        article.url = url
        article.save()


Base.metadata.create_all(Engine)
