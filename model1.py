from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Genre(Enum):
    Rock = 'Rock'
    Pop = 'Pop'
    Country = 'Country'
    Western = 'Western'


class UpdateArtistRequest(BaseModel):
    name: str
    genre: Genre


class Artist(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    genre: Optional[Genre] = None


class CreateArtistRequest(BaseModel):
    name: str
    genre: Genre
