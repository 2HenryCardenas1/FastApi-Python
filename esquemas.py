from pydantic import BaseModel,Field
from typing import Optional

class Movie(BaseModel):
    id : Optional[int] = None
    title : str = Field(..., min_length=1, max_length=50)
    overview : str = Field(..., min_length=1, max_length=500)
    year : int = Field(...,le=2021)
    rating : float = Field(...,ge=0.0,le=10.0)
    category : str = Field(..., min_length=1, max_length=20)

    class Config :
        json_schema_extra ={
            "example" : {
                "title" : "The Godfather",
                "overview" : "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
                "year" : 1972,
                "rating" : 9.2,
                "category" : "Drama"
            }
        }

class User(BaseModel):
    email : str = Field(..., min_length=1, max_length=50)
    password : str = Field(..., min_length=1, max_length=50)
    