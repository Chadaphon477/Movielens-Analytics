import streamlit as st
import pandas as pd
import bcrypt
from pymongo import MongoClient
from datetime import datetime

# ---------------- MongoDB Connection ----------------
MONGO_URI = "mongodb+srv://Chadaphon:12345678c@cluster0.19mnxif.mongodb.net/movielens?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["movielens"]

users_col   = db["users"]
logins_col  = db["logins"]
movies_col  = db["movies"]
ratings_col = db["ratings"]

# ---------- แผนที่ชื่อประเภทหนัง ----------
GENRE_MAP = {
    "0":"Action","1":"Adventure","2":"Animation","3":"Children",
    "4":"Comedy","5":"Crime","6":"Documentary","7":"Drama",
    "8":"Fantasy","9":"Film-Noir","10":"Horror","11":"Musical",
    "12":"Mystery","13":"Romance","14":"Sci-Fi","15":"Thriller",
    "16":"War","17":"Western","18":"IMAX","19":"Biography"
}

def normalize_genre(val) -> str:
    """แปลงค่า genre_8 หรือ 8 ให้เป็นชื่อประเภทหนัง"""
    if pd.isna(val):
        return "ไม่ระบุ"
    s = str(val).strip()
    if s.lower().startswith("genre_"):
        num = s.split("_", 1)[1]
        return GENRE_MAP.get(num, s)
    if s.isdigit():
        return GENRE_MAP.get(s, s)
    return s

# ---------------- Cache Data ----------------
@st.cache_data
def load_movies():
    df = pd.DataFrame(list(movies_col.find({}, {"_id": 0, "movie_id": 1, "title": 1, "genre": 1})))
    if not df.empty:
        df = df.rename(columns={"genre": "ประเภทหนัง"})
        df["ประเภทหนัง"] = df["ประเภทหนัง"].apply(normalize_genre)
    return df

@st.cache_data
def load_ratings():
    return pd.DataFrame(list(ratings_col.find({}, {"_id": 0, "movie_id": 1, "rating": 1})))

movies_df  = load_movies()
ratings_df = load_ratings()

# ---------------- Auth Functions ----------------
def register_user(username, password):
    if users_col.find_one({"username": username}):
        return False
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    users_col.insert_one({"username": username, "password": hashed_pw})
    return True

def login_user(username, password):
    user = users_col.find_one({"username": username})
    ok = bool(user and bcrypt.checkpw(password.encode("utf-8"), user["password"]))
    logins_col.insert_one({
        "username": username,
        "status": "success" if ok else "failed",
        "timestamp": datetime.now(),
        "ip": "unknown"
    })
    return ok

# ---------------- UI ----------------
st.set_page_config(page_title="MovieLens Dashboard", layout="wide")
st.title("🎬 MovieLens Dashboard")

if "auth" not in st.session_state:
    st.session_state["auth"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# ---------------- Login/Register ----------------
if not st.session_state["auth"]:
    choice = st.sidebar.radio("เลือกเมนู", ["Login", "Register"])

    if choice == "Login":
        st.subheader("🔑 เข้าสู่ระบบ")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(username, password):
                st.session_state["auth"] = True
                st.session_state["username"] = username
                st.success(f"ยินดีต้อนรับ {username} 👋")
                st.rerun()
            else:
                st.error("❌ Username หรือ Password ไม่ถูกต้อง")

    else:  # Register
        st.subheader("📝 สมัครสมาชิก")
        username = st.text_input("Username ใหม่")
        password = st.text_input("Password ใหม่", type="password")
        if st.button("Register"):
            if register_user(username, password):
                st.success("✅ สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ")
            else:
                st.error("❌ Username นี้ถูกใช้แล้ว")

# ---------------- Dashboard ----------------
else:
    menu = st.sidebar.radio(
        "เมนู",
        ["Home", "Movies", "Ratings", "Summary", "Top Movies", "Bottom Movies", "Genres Distribution", "Logout"]
    )

    # ----- Home -----
    if menu == "Home":
        st.header("🏠 Home")
        st.markdown("""
        ยินดีต้อนรับสู่ **MovieLens Dashboard**  
        ระบบนี้เชื่อมต่อกับ **FastAPI + MongoDB Atlas** และแสดงผลด้วย **Streamlit**

        **Tech Stack**
        - Backend: FastAPI, PyMongo, MongoDB Atlas  
        - Frontend: Streamlit, Pandas  
        - Auth: Register/Login (bcrypt) + เก็บ Log ลง MongoDB (`logins`)
        """)

    # ----- Movies -----
    elif menu == "Movies":
        st.header("🎬 Movies")
        total_movies  = len(movies_df)
        total_reviews = len(ratings_df)
        avg_rating    = ratings_df["rating"].mean() if not ratings_df.empty else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("📚 จำนวนหนัง", f"{total_movies:,}")
        c2.metric("📝 จำนวนรีวิว", f"{total_reviews:,}")
        c3.metric("⭐ ค่าเฉลี่ย Rating", f"{avg_rating:.2f}")

        st.subheader("📋 รายการหนังทั้งหมด")
        cols = [c for c in ["movie_id", "title", "ประเภทหนัง"] if c in movies_df.columns]
        st.dataframe(movies_df[cols])

    # ----- Ratings -----
    elif menu == "Ratings":
        st.header("⭐ Ratings")

        genres = ["ทั้งหมด"] + sorted(movies_df["ประเภทหนัง"].dropna().astype(str).unique())
        sel_genre = st.selectbox("เลือกประเภทหนัง", genres)

        merged_df = ratings_df.merge(movies_df, on="movie_id", how="left")

        if sel_genre != "ทั้งหมด":
            df_show = merged_df[merged_df["ประเภทหนัง"].astype(str) == sel_genre]
        else:
            df_show = merged_df

        st.subheader("Distribution of Ratings")
        if not df_show.empty:
            st.bar_chart(df_show["rating"].value_counts().sort_index())
        else:
            st.info("ไม่มีข้อมูลในประเภทที่เลือก")

        st.subheader("📋 ตารางค่าเฉลี่ย Rating ของภาพยนตร์")
        if not df_show.empty:
            avg_table = (
                df_show.groupby(["movie_id", "title", "ประเภทหนัง"])["rating"]
                .agg(["count", "mean"])
                .reset_index()
                .rename(columns={"count": "จำนวนรีวิว", "mean": "ค่าเฉลี่ย"})
                .sort_values("จำนวนรีวิว", ascending=False)
            )
            avg_table["ค่าเฉลี่ย"] = avg_table["ค่าเฉลี่ย"].round(2)
            st.dataframe(avg_table)
        else:
            st.info("ไม่มีข้อมูลสำหรับสร้างตาราง")

    # ----- Summary -----
    elif menu == "Summary":
        st.header("📊 Summary")
        merged = ratings_df.merge(movies_df, on="movie_id", how="left")
        if not merged.empty:
            summary = (
                merged.groupby("ประเภทหนัง")["rating"]
                .agg(["count", "mean"])
                .reset_index()
                .rename(columns={"count": "จำนวนรีวิว", "mean": "ค่าเฉลี่ย"})
                .sort_values("จำนวนรีวิว", ascending=False)
            )
            summary["ค่าเฉลี่ย"] = summary["ค่าเฉลี่ย"].round(2)
            st.dataframe(summary)
        else:
            st.info("ยังไม่มีข้อมูลสำหรับสรุป")

    # ----- Top Movies -----
    elif menu == "Top Movies":
        st.header("🏆 Top Movies")
        merged = ratings_df.merge(movies_df, on="movie_id", how="left")
        if not merged.empty:
            top_movies = (
                merged.groupby(["movie_id", "title", "ประเภทหนัง"])["rating"]
                .agg(["count", "mean"])
                .reset_index()
                .rename(columns={"count": "จำนวนรีวิว", "mean": "ค่าเฉลี่ย"})
                .sort_values("จำนวนรีวิว", ascending=False)
                .head(10)
            )
            top_movies["ค่าเฉลี่ย"] = top_movies["ค่าเฉลี่ย"].round(2)
            st.dataframe(top_movies)
        else:
            st.info("ยังไม่มีข้อมูลสำหรับ Top Movies")

    # ----- Bottom Movies -----
    elif menu == "Bottom Movies":
        st.header("📉 Bottom Movies")
        merged = ratings_df.merge(movies_df, on="movie_id", how="left")
        if not merged.empty:
            bottom_movies = (
                merged.groupby(["movie_id", "title", "ประเภทหนัง"])["rating"]
                .agg(["count", "mean"])
                .reset_index()
                .rename(columns={"count": "จำนวนรีวิว", "mean": "ค่าเฉลี่ย"})
                .sort_values("ค่าเฉลี่ย", ascending=True)
                .head(10)
            )
            bottom_movies["ค่าเฉลี่ย"] = bottom_movies["ค่าเฉลี่ย"].round(2)
            st.dataframe(bottom_movies)
        else:
            st.info("ยังไม่มีข้อมูลสำหรับ Bottom Movies")

    # ----- Genres Distribution -----
    elif menu == "Genres Distribution":
        st.header("📊 Genres Distribution")
        if not movies_df.empty:
            genre_counts = movies_df["ประเภทหนัง"].value_counts().reset_index()
            genre_counts.columns = ["ประเภทหนัง", "จำนวนหนัง"]
            st.bar_chart(genre_counts.set_index("ประเภทหนัง"))
            st.dataframe(genre_counts)
        else:
            st.info("ยังไม่มีข้อมูลประเภทหนัง")

    # ----- Logout -----
    else:
        st.session_state["auth"] = False
        st.session_state["username"] = ""
        st.success("👋 ออกจากระบบเรียบร้อย")
        st.rerun()
