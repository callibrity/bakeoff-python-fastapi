
from fastapi import Depends, FastAPI, HTTPException, Request, Response

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from db import engine, SessionLocal
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

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# Dependency
def get_db(request: Request):
    return request.state.db

@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})


@app.get('/api/artists/{id}', tags=["Artist"],response_model=schemas.Artist)
def get_artist(id: str, db: Session = Depends(get_db)):
    """
    Get all the Artists stored in database
    """
    db_artist = ArtistRepo.fetch_by_id(db, id)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found with the given ID")
    return db_artist


@app.put('/api/artists/{id}', tags=["Artist"], response_model=schemas.Artist)
async def update_artist(id: str, artist_request: schemas.UpdateArtistRequest, db: Session = Depends(get_db)):
    """
    Update an Artist stored in the database
    """
    db_artist = ArtistRepo.fetch_by_id(db, id)
    if db_artist:
        update_artist_encoded = jsonable_encoder(artist_request)
        db_artist.name = update_artist_encoded['name']
        db_artist.genre = update_artist_encoded['genre']
        return await ArtistRepo.update(db=db, artist=db_artist)
    else:
        raise HTTPException(status_code=400, detail="Artist not found with the given ID")


@app.delete('/api/artists/{id}', tags=["Item"])
async def delete_item(id: str, db: Session = Depends(get_db)):
    """
    Delete the ARtist with the given ID provided by User stored in database
    """
    db_artist = ArtistRepo.fetch_by_id(db, id)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found with the given ID")
    await ArtistRepo.delete(db, id)
    return "Artist deleted successfully!"


@app.post('/api/artists/', tags=["Artist"], response_model=schemas.Artist,status_code=200)
async def create_item(artist_request: schemas.CreateArtistRequest, db: Session = Depends(get_db)):
    """
    Create an Artist and store it in the database
    """
    return await ArtistRepo.create(db=db, artist=artist_request)


@app.get('/api/artists/', tags=["Artist"],response_model=List[schemas.Artist])
def get_all_artists(db: Session = Depends(get_db)):
    """
    Get all the Artists stored in database
    """
    return ArtistRepo.fetch_all(db)


if __name__ == "__main__":
    api_port = BakeOffEnvironmentVariables.api_port
    uvicorn.run("main:app", host='0.0.0.0', port=api_port, reload=False)
