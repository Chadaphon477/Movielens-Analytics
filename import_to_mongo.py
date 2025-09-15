import pandas as pd
from pymongo import MongoClient

# 1. เชื่อมต่อ MongoDB Atlas
client = MongoClient(
    "mongodb+srv://Chadaphon:12345678c@cluster0.19mnxif.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

# 2. เลือก Database และ Collection
db = client["moviedb"]          # ชื่อ Database
collection = db["movies"]       # ชื่อ Collection

# 3. โหลดข้อมูลจากไฟล์ CSV
df = pd.read_csv(r"D:\movielens\movies.csv")   # <-- แก้ path ให้ตรงกับไฟล์ของคุณ

# 4. Import ข้อมูลเข้า MongoDB
collection.insert_many(df.to_dict("records"))

print("✅ Import เสร็จเรียบร้อยแล้ว!")
