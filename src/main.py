from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse

from db import get_db, engine
import models as models
import schemas as schemas
from repositories import GenreRepo
from sqlalchemy.orm import Session
import uvicorn
from typing import List,Optional

app = FastAPI(title="Sample FastAPI Application",
              description="Sample FastAPI Application with Swagger and Sqlalchemy",
              version="1.0.0",)

models.Base.metadata.create_all(bind=engine)

@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})


@app.post('/genre', tags=["Genre"],response_model=schemas.Genre,status_code=201)
async def create_item(genre_request: schemas.GenreCreate, db: Session = Depends(get_db)):
    """
    Create a Genre and store it in the database
    """

    db_item = GenreRepo.fetch_by_name(db, name=genre_request.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Genre already exists!")

    return await GenreRepo.create(db=db, genre=genre_request)


@app.get('/genres', tags=["Genre"],response_model=List[schemas.Genre])
def get_all_genre(db: Session = Depends(get_db)):
    """
    Get all the Items stored in database
    """
    return GenreRepo.fetch_all(db)


if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)