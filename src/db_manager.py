from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, BINARY, TypeDecorator
import sqlite3
import io
from sqlalchemy.ext.declarative import declarative_base

import numpy as np

Base = declarative_base()


# Hackish to be able to store np.array into sqlite3
# https://stackoverflow.com/questions/18621513/python-insert-numpy-array-into-sqlite3-database
class ARRAY(TypeDecorator):
    impl = BINARY

    def process_bind_param(self, value, dialect):
        out = io.BytesIO()
        np.save(out, value)
        out.seek(0)
        return sqlite3.Binary(out.read())

    def process_result_value(self, value, dialect):
        out = io.BytesIO(value)
        out.seek(0)
        return np.load(out)


# table schema
class Poster(Base):
    __tablename__ = 'poster'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)
    url_img = Column(String, nullable=True)
    path_img = Column(String, nullable=True)
    path_thumb = Column(String, nullable=True)
    features = Column(ARRAY, nullable=True)

    def __init__(self, dict_poster=None):
        if dict_poster is None:
            pass
        else:
            self.title = dict_poster.get('title', '')
            self.url_img = dict_poster.get('url_img', '')
            self.path_img = dict_poster.get('path_img', '')
            self.path_thumb = dict_poster.get('path_thumb', '')
            self.features = dict_poster.get('features', np.array(None))


def get_db(uri):
    engine = create_engine(uri)
    if not engine.dialect.has_table(engine, 'poster'):
        Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def get_all_data(uri):
    db = get_db(uri)
    return db.query(Poster).all(), db
