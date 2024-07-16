from config.database import Session
from fastapi import APIRouter, Path, Query, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List

from apps.movie.schemas.movie import MovieSchema
from apps.movie.services.movie import MovieService
from middlewares.jwt_bearer import JWTBearer

movie_router = APIRouter()


# All movies
@movie_router.get("/movies", tags=["Movies"], response_model=List[MovieSchema], status_code=200, dependencies=[Depends(JWTBearer())])
# @movie_router.get("/movies", tags=["Movies"], response_model=List[MovieSchema], status_code=200)
def get_movies() -> List[MovieSchema]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


# Get movie Id
@movie_router.get("/movie/{id}", tags=["Movies"], response_model=MovieSchema, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> MovieSchema:
    db = Session()
    result = MovieService(db).get_movie_by_id(id)

    if not result:
        return JSONResponse(content={"message": "Pelicula no encontrada"}, status_code=404)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


# Get movie by category
@movie_router.get("/movie/", tags=["Movies"], response_model=List[MovieSchema], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[MovieSchema]:
    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@movie_router.post("/movie", tags=["Movies"], response_model=dict, status_code=201)
def create_movie(movie: MovieSchema) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(content={"message": "Se ha creado la Pelicula"}, status_code=201)


@movie_router.put('/movie/{id}', tags=['Movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: MovieSchema) -> dict:
    db = Session()
    response = MovieService(db).update_movie(id, movie)
    return JSONResponse(content={"message": response["message"]}, status_code=response["status_code"])


@movie_router.delete('/movie/{id}', tags=["Movies"], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    response = MovieService(db).delete_movie(id)
    return JSONResponse(content={"message": response["message"]}, status_code=response["status_code"])
