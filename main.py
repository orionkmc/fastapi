from fastapi import FastAPI, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "Mi primera API"
app.version = "0.1.0"


class Movie(BaseModel):
    id: Optional[int] = None
    title : str = Field(min_length=5, max_length=15)
    overview : str = Field(min_length=15, max_length=50)
    year : int = Field(Le=2022)
    rating : float = Field(ge=1, le=10)
    category : str = Field(min_length=5, max_length=15)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
               {
                'id': 1,
                'title' : 'Crepusculo',
                'overview' : 'The twilight is almost better than sunday',
                'year' : '2022',
                'rating' : 9.5,
                'category' : 'Phantasy'
            }
            ]
        }
    }

movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus pellentesque vel lorem ut ultrices. Nullam odio neque, aliquet sed ullamcorper ut, cursus vitae urna. Morbi vehicula eros augue, sit amet pellentesque libero faucibus nec.",
        "year": "2009",
        "rating": 7.8,
        "category": "Accion",
    },
    {
        "id": 2,
        "title": "Avatar",
        "overview": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus pellentesque vel lorem ut ultrices. Nullam odio neque, aliquet sed ullamcorper ut, cursus vitae urna. Morbi vehicula eros augue, sit amet pellentesque libero faucibus nec.",
        "year": "2009",
        "rating": 7.8,
        "category": "Emocion",
    }
]


@app.get("/", tags=["Home"], response_model=str, status_code=200)
def home():
    return JSONResponse(content="hola mundooooo", status_code=200)


@app.get("/movies", tags=["movies"], response_model=List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies, status_code=200)


@app.get("/movies/{id}", tags=["movies"], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    for movie in movies:
        if movie["id"] == id:
            return JSONResponse(content=movie, status_code=200)
    return JSONResponse(content=[], status_code=400)


@app.get("/movies/", tags=["movies"], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [movie for movie in movies if movie["category"] == category]
    return JSONResponse(content=data, status_code=200)


@app.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(content={ "message": "Se ha creado la Pelicula" }, status_code=201)


@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(content={ "message": "Se ha modificado la Pelicula" }, status_code=200)
    return JSONResponse(content={ "message": "NO se ha encontrado la Pelicula" }, status_code=200)


@app.delete('/movies/{id}', tags=["movies"], response_model=dict, status_code=200)
def delete_movie(id : int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            JSONResponse(content={ "message": "Se ha eliminado la Pelicula" }, status_code=200)
    return JSONResponse(content={ "message": "NO se ha encontrado la Pelicula" }, status_code=200)