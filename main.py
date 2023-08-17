from typing import List

from fastapi import Body, Depends, FastAPI, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer

from constanst import _SECRET_KEY
from esquemas import Movie, User
from jwtManager import JwtManager

app = FastAPI()

app.title = "Movies API"
app.description = "API for movies"
app.version = "0.0.1"


jwt = JwtManager(_SECRET_KEY)


movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción",
    },
    {
        "id": 2,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
        "rating": 7.823,
        "category": "Acción",
    },
]


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = jwt.validate_token(auth.credentials)

        if data["email"] != "admin@admim.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")


@app.post("/login", tags=["Auth"])
def login(user: User):
    if user.email == "admin@admim.com" and user.password == "admin":
        token = jwt.create_token({"email": user.email})
        return JSONResponse(
            content={"message": "Login success", "token": token}, status_code=200
        )


@app.get("/", tags=["Home"])
def message():
    return HTMLResponse(content="<h1>Welcome to the Movies API</h1>", status_code=200)


# Json response


@app.get(
    "/movies",
    tags=["Movies"],
    response_model=List[Movie],
    dependencies=[Depends(JWTBearer())],
)
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies, status_code=200)


# Path parameters


@app.get("/movie/{id}", tags=["Movies"], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    for movie in movies:
        if movie["id"] == id:
            return JSONResponse(content=movie, status_code=200)
    return JSONResponse(content={"message": "Movie not found"}, status_code=404)


# Query parameters


@app.get("/movies/", tags=["Movies"], response_model=List[Movie])
def get_movies_by_category(
    category: str = Query(min_length=1, max_length=20)
) -> List[Movie]:
    movies_by_category = []
    for movie in movies:
        if movie["category"] == category:
            movies_by_category.append(movie)

    if len(movies_by_category) > 0:
        return JSONResponse(content=movies_by_category, status_code=200)
    else:
        return JSONResponse(content={"message": "Category not found"}, status_code=404)


@app.post("/movies", tags=["Movies"])
def create_movie(movie: Movie):
    movies.append(movie)
    return JSONResponse(content={"message": "Movie created"}, status_code=201)


@app.put("/movies/{id}", tags=["Movies"])
def update_movie(movie: Movie, id: int):
    for movie in movies:
        if movie["id"] == id:
            movie["title"] = movie.title
            movie["overview"] = movie.overview
            movie["year"] = movie.year
            movie["rating"] = movie.rating
            movie["category"] = movie.category
            return JSONResponse(content=movie, status_code=200)

    return JSONResponse(content={"message": "Movie not found"}, status_code=404)


@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int):
    for movie in movies:
        if movie["id"] == id:
            movies.remove(movie)
            return JSONResponse(content={"message": "Movie deleted"}, status_code=200)
    return JSONResponse(content={"message": "Movie not found"}, status_code=404)
