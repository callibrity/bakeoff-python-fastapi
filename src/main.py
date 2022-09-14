from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse

from db import get_db, engine
import models as models
import schemas as schemas
from repositories import ArtistRepo
from sqlalchemy.orm import Session
import uvicorn
from typing import List

app = FastAPI(title="Sample FastAPI Application",
              description="Sample FastAPI Application with Swagger and Sqlalchemy",
              version="1.0.0",)

models.Base.metadata.create_all(bind=engine)

@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})


@app.post('/artists', tags=["Artist"],response_model=schemas.Artist,status_code=201)
async def create_item(artist_request: schemas.CreateArtistRequest, db: Session = Depends(get_db)):
    """
    Create a Artist and store it in the database
    """

    db_item = ArtistRepo.fetch_by_name(db, name=artist_request.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Artist already exists!")

    return await ArtistRepo.create(db=db, artist=artist_request)


@app.get('/api/artists/', tags=["Artist"],response_model=List[schemas.Artist])
def get_all_artists(db: Session = Depends(get_db)):
    """
    Get all the Items stored in database
    """
    return ArtistRepo.fetch_all(db)


if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)