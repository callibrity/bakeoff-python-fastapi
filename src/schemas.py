from typing import List, Optional
from enum import Enum

from pydantic import BaseModel


class Genre(str, Enum):
    Rock = 'Rock'
    Pop = 'Pop'
    Country = 'Country'
    Western = 'Western'


class ArtistBase(BaseModel):
    id: Optional[str] = None
    name: str = None
    genre: Genre = None

class Artist(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    genre: Optional[Genre] = None

    class Config:
        orm_mode = True

class CreateArtistRequest(ArtistBase):
    pass

class UpdateArtistRequest(BaseModel):
    name: str
    genre: Genre

