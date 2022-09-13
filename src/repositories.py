
from sqlalchemy.orm import Session

import models, schemas


class GenreRepo:

    async def create(db: Session, genre: schemas.GenreCreate):
        db_genre = models.Genre(name=genre.name)
        db.add(db_genre)
        db.commit()
        db.refresh(db_genre)
        return db_genre

    def fetch_by_id(db: Session,_id):
        return db.query(models.Genre).filter(models.Genre.id == _id).first()

    def fetch_by_name(db: Session,name):
        return db.query(models.Genre).filter(models.Genre.name == name).first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Genre).offset(skip).limit(limit).all()

    async def delete(db: Session,genre_id):
        db_genre= db.query(models.Genre).filter_by(id=genre_id).first()
        db.delete(db_genre)
        db.commit()


    async def update(db: Session,genre_data):
        updated_genre = db.merge(genre_data)
        db.commit()
        return updated_genre



class ArtistRepo:

    async def create(db: Session, artist: schemas.ArtistCreate):
        db_artist = models.Artist(name=artist.name)
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

    async def update(db: Session,artist_data):
        db.merge(artist_data)
        db.commit()