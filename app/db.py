from pymongo import MongoClient

# 🔗 MongoDB Atlas Connection
MONGO_URI = "mongodb+srv://Chadaphon:12345678c@cluster0.19mnxif.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)

# เลือก Database
db = client["movielens"]

# ✅ Collections
movies_collection = db["movies"]
ratings_collection = db["ratings"]
users_collection = db["users"]

# ✅ Debug log
if __name__ == "__main__":
    print("✅ Connected to MongoDB Atlas")
    print("Database:", db.name)
    print("Collections:", db.list_collection_names())
