from pymongo import MongoClient

# 🔗 Connection String
client = MongoClient(
    "mongodb+srv://Chadaphon:12345678c@cluster0.19mnxif.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

# เลือก Database
db = client["movielens"]

print("✅ Connected to MongoDB Atlas")
print("Database:", db.name)

# -------------------------------
# 🎬 Movies Collection
# -------------------------------
movies = db["movies"]
print(f"\n🎬 movies count: {movies.count_documents({})}")
for m in movies.find().limit(5):
    print(m)

# -------------------------------
# ⭐ Ratings Collection
# -------------------------------
ratings = db["ratings"]
print(f"\n⭐ ratings count: {ratings.count_documents({})}")
for r in ratings.find().limit(5):
    print(r)

# -------------------------------
# 👤 Users Collection
# -------------------------------
users = db["users"]
print(f"\n👤 users count: {users.count_documents({})}")
for u in users.find().limit(5):
    print(u)
