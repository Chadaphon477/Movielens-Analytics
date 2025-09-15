from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel
from typing import Optional

# ---------- Database Connection ----------
client = MongoClient("mongodb+srv://Chadaphon:12345678c@cluster0.19mnxif.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["movielens"]
movies = db["movies"]

# ---------- FastAPI ----------
app = FastAPI()

# ---------- Pydantic Model ----------
class Movie(BaseModel):
    movie_id: Optional[int]
    title: str
    release_year: int
    duration: int
    genre: str

# ---------- Routes ----------
@app.get("/")
def root():
    return {"message": "API is running 🚀"}

# 1. GET all movies
@app.get("/movies")
def get_movies():
    data = []
    for m in movies.find():
        m["_id"] = str(m["_id"])  # แปลง ObjectId ให้เป็น string
        data.append(m)
    return data

# 2. GET movie by id
@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    movie = movies.find_one({"movie_id": movie_id})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie["_id"] = str(movie["_id"])
    return movie

# 3. POST new movie
@app.post("/movies")
def create_movie(movie: Movie):
    movie_dict = movie.dict()
    result = movies.insert_one(movie_dict)
    return {"message": "Movie added", "id": str(result.inserted_id)}

# 4. PUT update movie
@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, movie: Movie):
    updated = movies.update_one({"movie_id": movie_id}, {"$set": movie.dict()})
    if updated.matched_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie updated"}

# 5. DELETE movie
@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    deleted = movies.delete_one({"movie_id": movie_id})
    if deleted.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted"}
