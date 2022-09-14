
from sqlalchemy.orm import Session

import models, schemas


class ArtistRepo:

    async def create(db: Session, artist: schemas.CreateArtistRequest):
        db_artist = models.Artist(name=artist.name, genre=artist.genre)
        db.add(db_artist)
        db.commit()
        db.refresh(db_artist)
        return db_artist

    def fetch_by_id(db: Session,_id:int):
        return db.query(models.Artist).filter(models.Artist.id == _id).first()

    def fetch_by_name(db: Session,name:str):
        return db.query(models.Artist).filter(models.Artist.name == name).first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Artist).offset(skip).limit(limit).all()

    async def delete(db: Session,_id:int):
        db_artist= db.query(models.Artist).filter_by(id=_id).first()
        db.delete(db_artist)
        db.commit()

    async def update(db: Session, artist: schemas.UpdateArtistRequest):
        db_artist = models.Artist(id=artist.id, name=artist.name, genre=artist.genre)
        db_updated_artist = db.merge(db_artist)
        db.commit()
        return db_updated_artist
