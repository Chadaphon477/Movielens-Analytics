import pandas as pd
import os

# 📂 Path ของโฟลเดอร์ ml-100k
data_path = "C:/Users/user/Downloads/ml-100k/ml-100k/"
# ✅ เช็คว่าไฟล์ u.user อยู่จริงหรือไม่
print("Check u.user:", os.path.exists(data_path + "u.user"))

# ---------- USERS ----------
print("📥 Loading u.user ...")
users = pd.read_csv(
    data_path + "u.user",
    sep="|",
    names=["user_id", "age", "gender", "occupation", "zipcode"],
    encoding="latin-1"
)

# เพิ่ม field 
users["name"] = "User" + users["user_id"].astype(str)
users["email"] = users["name"].str.lower() + "@example.com"
users["join_date"] = pd.Timestamp.today().strftime("%Y-%m-%d")

users.to_csv("users.csv", index=False)
print("✅ users.csv created")

# ---------- MOVIES ----------
print("📥 Loading u.item ...")
movies = pd.read_csv(
    data_path + "u.item",
    sep="|",
    names=["movie_id", "title", "release_date", "video_release_date", "IMDb_URL"] + [f"genre_{i}" for i in range(19)],
    encoding="latin-1"
)

# ดึงปีจาก release_date
movies["release_year"] = movies["release_date"].str[-4:]
movies["duration"] = 120  # mock duration
movies["genre"] = movies[[f"genre_{i}" for i in range(19)]].idxmax(axis=1)

movies = movies[["movie_id", "title", "release_year", "duration", "genre"]]
movies.to_csv("movies.csv", index=False)
print("✅ movies.csv created")

# ---------- RATINGS ----------
print("📥 Loading u.data ...")
ratings = pd.read_csv(
    data_path + "u.data",
    sep="\t",
    names=["user_id", "movie_id", "rating", "timestamp"],
    encoding="latin-1"
)

ratings["rating_date"] = pd.to_datetime(ratings["timestamp"], unit="s").dt.date
ratings = ratings[["user_id", "movie_id", "rating", "rating_date"]]
ratings.to_csv("ratings.csv", index=False)
print("✅ ratings.csv created")

print("🎉 Conversion Completed! Files ready: users.csv, movies.csv, ratings.csv")
