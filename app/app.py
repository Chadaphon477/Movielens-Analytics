from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional, List

# -------------------------------
# 🔗 Connect MongoDB
# -------------------------------
client = MongoClient(
    "mongodb+srv://Chadaphon:12345678c@cluster0.19mnxif.mongodb.net/"
    "?retryWrites=true&w=majority&appName=Cluster0"
)
db = client["movielens"]

movies = db["movies"]
ratings = db["ratings"]

# -------------------------------
# ⚡ FastAPI
# -------------------------------
app = FastAPI(title="MovieLens API", version="2.0.0")

# -------------------------------
# 🎬 Models
# -------------------------------
class Movie(BaseModel):
    movie_id: int
    title: str
    release_year: int
    duration: int
    genre: str

class Rating(BaseModel):
    user_id: int
    movie_id: int
    rating: float
    timestamp: Optional[int]

# -------------------------------
# 🟢 Root
# -------------------------------
@app.get("/")
def root():
    return {"message": "MovieLens API is running 🚀"}

# -------------------------------
# 🎞 Movies Endpoints
# -------------------------------
@app.get("/movies")
def get_movies():
    data = []
    for m in movies.find({}, {"_id": 0}):
        data.append(m)
    return data

@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    movie = movies.find_one({"movie_id": movie_id}, {"_id": 0})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.get("/movies/search")
def search_movies(
    genre: Optional[str] = None,
    year: Optional[int] = None,
    title: Optional[str] = None
):
    query = {}
    if genre:
        query["genre"] = genre
    if year:
        query["release_year"] = year
    if title:
        query["title"] = {"$regex": title, "$options": "i"}

    results = list(movies.find(query, {"_id": 0}))
    if not results:
        raise HTTPException(status_code=404, detail="No movies found")
    return results

# -------------------------------
# ⭐ Ratings Endpoints
# -------------------------------
@app.get("/ratings")
def get_ratings():
    data = []
    for r in ratings.find({}, {"_id": 0}):
        data.append(r)
    return data

@app.get("/ratings/{movie_id}")
def get_ratings_by_movie(movie_id: int):
    data = list(ratings.find({"movie_id": movie_id}, {"_id": 0}))
    if not data:
        raise HTTPException(status_code=404, detail="No ratings found for this movie")
    return data
