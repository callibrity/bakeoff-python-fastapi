import enum

from sqlalchemy import Column, Integer, String, Enum

from db import Base


class Genre(str, enum.Enum):
    Rock = 'Rock'
    Pop = 'Pop'
    Country = 'Country'
    Western = 'Western'


class Artist(Base):
    __tablename__ = 'artist'
    id = Column(String(80), primary_key=True, index=True)
    name = Column(String(80), nullable=False, unique=False)
    genre: Genre = Column(Enum(Genre))

    def __repr__(self):
        return 'Artist(name=%s)' % self.name
