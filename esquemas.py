from pydantic import BaseModel,Field
from typing import Optional

class Movie(BaseModel):
    id : Optional[int] = None
    title : str = Field(..., min_length=1, max_length=50)
    overview : str | None = None
    year : str
    rating : float | None = None
    category : str