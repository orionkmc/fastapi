from fastapi import FastAPI

from apps.movie.routers.movie import movie_router
from apps.user.routers.auth import user_router
from apps.basic.router import basic_router
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler

app = FastAPI()
app.title = "API Movies"
app.version = "0.1.0"
app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)
app.include_router(basic_router)

Base.metadata.create_all(bind=engine)
