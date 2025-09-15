  # 🎬 MovieLens Dashboard

โปรเจ็กต์นี้คือ **MovieLens Dashboard** ที่เชื่อมต่อกับ **FastAPI + MongoDB Atlas** และแสดงผลด้วย **Streamlit**  
มีระบบ **สมัครสมาชิก, ล็อกอิน, ล็อกเอาต์** พร้อมเก็บ Log การใช้งานลง MongoDB  

---

## 🚀 Tech Stack

- **Backend**: FastAPI, PyMongo, MongoDB Atlas  
- **Frontend**: Streamlit, Pandas  
- **Authentication**: bcrypt, MongoDB logging  
- **Database**: MongoDB Atlas  

---

## 📂 Features (เมนูใน Dashboard)

- 🏠 **Home** → หน้าต้อนรับ + อธิบาย Tech Stack  
- 🎬 **Movies** → แสดงจำนวนหนัง, จำนวนรีวิว, ค่าเฉลี่ยเรทติ้ง, ตารางหนังทั้งหมด  
- ⭐ **Ratings** → เลือกประเภทหนังเพื่อดูการกระจายคะแนน และตารางค่าเฉลี่ยเรทติ้ง  
- 📊 **Summary** → ตารางสรุปรีวิวตามประเภทหนัง (จำนวนรีวิว + ค่าเฉลี่ย)  
- 🏆 **Top Movies** → 10 หนังที่มีจำนวนรีวิวมากที่สุด  
- 📉 **Bottom Movies** → 10 หนังที่ค่าเฉลี่ยเรทติ้งต่ำที่สุด  
- 📊 **Genres Distribution** → กราฟและตารางการกระจายของประเภทหนัง  
- 🔑 **Login/Register/Logout** → ระบบสมัคร, ล็อกอิน, ล็อกเอาต์  

## สร้าง Virtual Environment
**python -m venv venv**
**venv\Scripts\activate**     # Windows
**source venv/bin/activate** # Mac/Linux
**ติดตั้ง Dependencies**
**pip install -r requirements.txt**

## รัน FastAPI (API)
**python -m uvicorn app.app:app --reload**


**API จะรันที่ http://127.0.0.1:8000**

## รัน Streamlit Dashboard
**python -m streamlit run dashboard.py**


## Dashboard จะรันที่ http://localhost:8501

**📊 ตัวอย่างหน้าจอ**
**🔑 Login / Register**

**🎬 Movies**

**⭐ Ratings**

**📊 Summary**

**🏆 Top Movies**

**📉 Bottom Movies**

**📊 Genres Distribution**

📦 โครงสร้างไฟล์
MOVIELENS/
│── app/ (FastAPI backend)
│   ├── app.py
│   ├── api.py
│   ├── db.py
│── data/ (movies.csv, ratings.csv)
│── images/ (login.png, movies.png, ratings.png, summary.png, top_movies.png, bottom_movies.png, genres.png)
│── dashboard.py
│── import_to_mongo.py
│── test_connection.py
│── requirements.txt
│── run_dashboard.bat
│── README.md
│── .gitignore
│── .gitattributes


## 🚀 Tech Stack
- **Language**: Python 3.11  
- **Frontend**: Streamlit  
- **Backend**: FastAPI  
- **Database**: MongoDB Atlas (เชื่อมต่อผ่าน PyMongo)  
- **Data Processing**: Pandas  
- **Authentication**: bcrypt + MongoDB log  
- **Visualization**: Streamlit Components (เช่น bar_chart, dataframe)
