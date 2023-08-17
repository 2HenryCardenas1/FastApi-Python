from fastapi import Body, FastAPI, Path,Query
from fastapi.responses import HTMLResponse

from esquemas import Movie

app = FastAPI()

app.title = "Movies API"
app.description = "API for movies"
app.version = "0.0.1"


movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.823,
        'category': 'Acción'    
    } 
    ]


@app.get("/", tags=["Home"])
def message () :
    return HTMLResponse(content="<h1>Welcome to the Movies API</h1>", status_code=200)

@app.get("/movies", tags=["Movies"])
def get_movies () :
     return {"message": "Get all movies",
            "movies": movies}

# Path parameters

@app.get("/movie/{id}", tags=["Movies"])
def get_movie (id: int = Path(ge=1, le=2000)) :
    for movie in movies:
        if movie["id"] == id:
            return {"message": "Get movie by id",
            "movie": movie}
    return {"message": "Movie not found"}

# Query parameters

@app.get('/movies/', tags=["Movies"])
def get_movies_by_category( category : str = Query( min_length=1, max_length=20)):
    movies_by_category = []
    for movie in movies:
        if movie['category'] == category:
            movies_by_category.append(movie)

    if len(movies_by_category) > 0:
        return {"message": "Get movies by category",
                "movies": movies_by_category}
    else:
        return {"message": "Category not found"}
    
@app.post("/movies", tags=["Movies"])
def create_movie(movie : Movie):
    movies.append(movie)
    return {"message": "Create movie"}

@app.put("/movies/{id}", tags=["Movies"])
def update_movie(movie : Movie, id : int):
   
    for movie in movies:
       
        if movie["id"] == id:
            
            movie["title"] = movie.title
            movie["overview"] = movie.overview
            movie["year"] = movie.year
            movie["rating"] = movie.rating
            movie["category"] = movie.category
            return {"message": "Update movie", "movie": movie}
    
    return {"message": "Movie not found"}
        


@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id : int):
    for movie in movies:
        if movie["id"] == id:
            movies.remove(movie)
            return {"message": "Delete movie", "movie": movie}
    return {"message": "Movie not found"}