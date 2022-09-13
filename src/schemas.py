from typing import List, Optional

from pydantic import BaseModel


class GenreBase(BaseModel):
    name: str
    #artist_id: int


class GenreCreate(GenreBase):
    pass


class Genre(GenreBase):
    id: int

    class Config:
        orm_mode = True


class ArtistBase(BaseModel):
    name: str

class ArtistCreate(ArtistBase):
    pass

class Artist(ArtistBase):
    id: int
    genre: List[Genre] = []

    class Config:
        orm_mode = True