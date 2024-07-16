from apps.movie.models.movie import Movie as MovieModel
from apps.movie.schemas.movie import MovieSchema


class MovieService():
    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self):
        return self.db.query(MovieModel).all()

    def get_movie_by_id(self, id):
        movie_db = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        if not movie_db:
            return {"message": "Pelicula no encontrada", "status_code": 404}

        return movie_db

    def get_movie_by_category(self, category):
        return self.db.query(MovieModel).filter(MovieModel.category == category).all()

    def create_movie(self, movie: MovieSchema):
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        return

    def update_movie(self, id: int, movie: MovieSchema):
        movie_db = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        if not movie_db:
            return {"message": "Pelicula no encontrada", "status_code": 404}

        movie_db.title = movie.title
        movie_db.overview = movie.overview
        movie_db.year = movie.year
        movie_db.rating = movie.rating
        movie_db.category = movie.category
        self.db.commit()
        return {"message": "Se ha modificado la Pelicula", "status_code": 200}

    def delete_movie(self, id: int):
        movie_db = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        if not movie_db:
            return {"message": "Pelicula no encontrada", "status_code": 404}

        self.db.delete(movie_db)
        self.db.commit()
        return {"message": "Se ha eliminado la Pelicula", "status_code": 200}
