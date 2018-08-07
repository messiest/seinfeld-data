import os
import csv

from inflection import underscore
from sqlalchemy import create_engine, Column, String, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

import credentials


def str2int(s):
    try:
        return int(float(s))
    except ValueError:
        return s


seinfeld_db = {
    'drivername': credentials.drivername,
    'username': credentials.username,
    'password': credentials.password,
    'host': credentials.host,
    'port': credentials.port,
    'database': credentials.database,
}

db = create_engine(URL(**seinfeld_db))


Base = declarative_base()

Session = sessionmaker(db)
session = Session()


class Episode(Base):
    __tablename__ = 'episodes'

    season = Column(Integer)
    episode_no = Column(Integer)
    title = Column(String)
    air_date = Column(String)
    writers = Column(String)
    director = Column(String)
    seid = Column(String, primary_key=True)


class Script(Base):
    __tablename__ = 'scripts'

    season = Column(String)
    episode_no = Column(String)
    seid = Column(String, ForeignKey('episodes.seid'))
    character = Column(Text)
    dialogue = Column(Text)
    row_num = Column(Integer, primary_key=True)


Base.metadata.create_all(db)

# Episodes
with open(os.path.join('data', 'episode_info.csv'), 'r') as file:
    data = list(csv.reader(file.readlines()))
    headers = []
    for row in data:
        row = row[1:]
        if not headers:
            headers = [underscore(x) for x in row]
            continue
        row = [str2int(x) for x in row]
        row = dict(zip(headers, row))

        episode = Episode(**row)

        session.add(episode)

    session.commit()

# Scripts
with open(os.path.join('data', 'scripts.csv'), 'r') as file:
    data = list(csv.reader(file.readlines()))
    headers = []
    for row in data:
        if not headers:
            headers = [underscore(x) for x in row]
            headers[0] = 'row_num'
            continue
        row = [str2int(x) for x in row]
        row = dict(zip(headers, row))

        script = Script(**row)

        session.add(script)

    session.commit()
