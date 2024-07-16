from fastapi import APIRouter, Path, Query, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from config.database import Session
from models.movie import Movie as MovieModel
from middlewares.jwt_bearer import JWTBearer
from typing import List

movie_router = APIRouter()


class Movie(BaseModel):
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=200)
    year: int = Field(Le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "category": "Phantasy",
                "overview": "The twilight is almost better than sunday",
                "rating": 9.5,
                "title": "Crepusculo",
                "year": "2022"
            }]
        }
    }


# All movies
@movie_router.get("/movies", tags=["Movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
# @app.get("/movies", tags=["Movies"], response_model=List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


# Get movie Id
@movie_router.get("/movie/{id}", tags=["Movies"], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()

    if not result:
        return JSONResponse(content={"message": "Pelicula no encontrada"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


# Get movie by category
@movie_router.get("/movie/", tags=["Movies"], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        return JSONResponse(content={"message": "Pelicula no encontrada"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@movie_router.post("/movie", tags=["Movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(content={"message": "Se ha creado la Pelicula"}, status_code=201)


@movie_router.put('/movie/{id}', tags=['Movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    movie_db = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not movie_db:
        return JSONResponse(content={"message": "Pelicula no encontrada"}, status_code=404)

    movie_db.title = movie.title
    movie_db.overview = movie.overview
    movie_db.year = movie.year
    movie_db.rating = movie.rating
    movie_db.category = movie.category
    db.commit()
    return JSONResponse(content={"message": "Se ha modificado la Pelicula"}, status_code=200)


@movie_router.delete('/movie/{id}', tags=["Movies"], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    movie_db = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not movie_db:
        return JSONResponse(content={"message": "Pelicula no encontrada"}, status_code=404)
    db.delete(movie_db)
    db.commit()
    return JSONResponse(content={"message": "Se ha eliminado la Pelicula"}, status_code=200)
