import os
import csv

from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

import credentials


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


print(db)

Session = sessionmaker(db)
session = Session()


class Episode(Base):
    __tablename__ = 'episodes'

    Season = Column(String)
    EpisodeNo = Column(String)
    Title = Column(String)
    AirDate = Column(String)
    Writers = Column(String)
    Director = Column(String)
    SEID = Column(String, primary_key=True)


Base.metadata.create_all(db)


with open(os.path.join('data', 'episode_info.csv'), 'r') as file:
    data = list(csv.reader(file.readlines()))


headers = []
for row in data:
    row = row[1:]
    if not headers:
        headers = row
        continue
    row = dict(zip(headers, row))

    episode = Episode(**row)

    session.add(episode)

session.commit()
