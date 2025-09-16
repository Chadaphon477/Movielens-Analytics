import pandas as pd
from pymongo import MongoClient

#เชื่อมต่อ MongoDB Atlas
client = MongoClient(
    "mongodb+srv://Chadaphon:12345678c@cluster0.19mnxif.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

#เลือก Database และ Collection
db = client["moviedb"]          # ชื่อ Database
collection = db["movies"]       # ชื่อ Collection

#โหลดข้อมูลจากไฟล์ CSV
df = pd.read_csv(r"D:\movielens\movies.csv")   

#Import ข้อมูลเข้า MongoDB
collection.insert_many(df.to_dict("records"))

print("✅ Import เสร็จเรียบร้อยแล้ว!")
