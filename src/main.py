from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from db import get_db, engine
import models as models
import schemas as schemas
from repositories import ArtistRepo
from sqlalchemy.orm import Session
import uvicorn
from typing import List
from variables import BakeOffEnvironmentVariables

app = FastAPI(title="Bakeoff FastAPI Application",
              description="FastAPI Application with Swagger and Sqlalchemy",
              version="1.0.0",)

models.Base.metadata.create_all(bind=engine)


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})


@app.get('/api/artists/{id}', tags=["Artist"],response_model=schemas.Artist)
def get_artist(artist_id: str, db: Session = Depends(get_db)):
    """
    Get all the Artists stored in database
    """
    db_artist = ArtistRepo.fetch_by_id(db, artist_id)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found with the given ID")
    return db_artist


@app.put('/api/artists/{artist_id}', tags=["Artist"], response_model=schemas.Artist)
async def update_artist(artist_id: str, artist_request: schemas.UpdateArtistRequest, db: Session = Depends(get_db)):
    """
    Update an Artist stored in the database
    """
    db_artist = ArtistRepo.fetch_by_id(db, artist_id)
    if db_artist:
        update_artist_encoded = jsonable_encoder(artist_request)
        db_artist.name = update_artist_encoded['name']
        db_artist.genre = update_artist_encoded['genre']
        return await ArtistRepo.update(db=db, artist=db_artist)
    else:
        raise HTTPException(status_code=400, detail="Artist not found with the given ID")


@app.delete('/api/artists/{artist_id}', tags=["Item"])
async def delete_item(artist_id: str, db: Session = Depends(get_db)):
    """
    Delete the ARtist with the given ID provided by User stored in database
    """
    db_artist = ArtistRepo.fetch_by_id(db, artist_id)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found with the given ID")
    await ArtistRepo.delete(db, artist_id)
    return "Artist deleted successfully!"


@app.post('/api/artists', tags=["Artist"], response_model=schemas.Artist,status_code=201)
async def create_item(artist_request: schemas.CreateArtistRequest, db: Session = Depends(get_db)):
    """
    Create an Artist and store it in the database
    """
    db_item = ArtistRepo.fetch_by_name(db, name=artist_request.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Artist already exists!")

    return await ArtistRepo.create(db=db, artist=artist_request)


@app.get('/api/artists/', tags=["Artist"],response_model=List[schemas.Artist])
def get_all_artists(db: Session = Depends(get_db)):
    """
    Get all the Artists stored in database
    """
    return ArtistRepo.fetch_all(db)


if __name__ == "__main__":
    api_port = BakeOffEnvironmentVariables.api_port
    uvicorn.run("main:app", port=api_port, reload=False)