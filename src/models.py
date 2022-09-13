from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from db import Base

class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(80), nullable=False, unique=True,index=True)
    def __repr__(self):
        return 'GenreModel(name=%s)' % (self.name)

class Artist(Base):
    __tablename__ = "artist"
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(80), nullable=False, unique=True)
    #genres = relationship("Genre",primaryjoin="Artist.id == Genre.artist_id",cascade="all, delete-orphan")

    def __repr__(self):
        return 'Artist(name=%s)' % self.name
    