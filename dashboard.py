import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud
import io
import re
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# =========================
# ตั้งค่าเพจ
# =========================
st.set_page_config(page_title="MovieLens Dashboard", page_icon="🎬", layout="wide")

# =========================
# โหลดไฟล์ CSV แบบปลอดภัย
# =========================
BASE_DIR = os.path.dirname(__file__)
movies = pd.read_csv(os.path.join(BASE_DIR, "data", "movies.csv"))
ratings = pd.read_csv(os.path.join(BASE_DIR, "data", "ratings.csv"))
users   = pd.read_csv(os.path.join(BASE_DIR, "data", "users.csv"))

# Extract year from movie title
movies["year"] = movies["title"].str.extract(r'\((\d{4})\)').astype(float)

# รวมข้อมูล
df = ratings.merge(movies, on="movie_id").merge(users, on="user_id")

# =========================
# Streamlit UI
# =========================
tab_home, tab1, tab2, tab4, tab5, tab6 = st.tabs([
    "🏠 Home",
    "📊 Top Movies", 
    "☁️ Word Cloud", 
    "🤖 Recommendation System",
    "💬 Q&A System",
    "🔮 Predict Rating"
])

# -------------------------
# Tab Home (Landing Page)
# -------------------------
with tab_home:
    st.image("https://raw.githubusercontent.com/github/explore/main/topics/movie/movie.png", width=120)
    st.title("🎬 MovieLens Interactive Dashboard")
    st.markdown("""
    ยินดีต้อนรับสู่ **MovieLens Dashboard** 🚀  

    โปรเจ็กต์นี้สร้างขึ้นเพื่อ:
    - วิเคราะห์ข้อมูลภาพยนตร์จาก MovieLens Dataset  
    - แสดงผลข้อมูลในรูปแบบ Interactive Dashboard  
    - สาธิตการประยุกต์ใช้ AI/ML ใน Recommendation & Prediction  
    """)

    # ✅ Tech Stack แบบกดขยาย/ย่อได้
    with st.expander("👨‍💻 Tech Stack"):
        st.markdown("""
        - Python, Pandas, Numpy  
        - Streamlit, Matplotlib, WordCloud  
        - Scikit-learn (Machine Learning)  
        """)

# -------------------------
# Tab 1: Top Movies
# -------------------------
with tab1:
    st.header("Top Movies by Year, Gender, and Age")

    years = sorted(movies["year"].dropna().unique())
    year = st.sidebar.selectbox("เลือกปีที่ต้องการดู", years)

    top_n = st.sidebar.slider("จำนวน Top Movies", 5, 20, 10)

    gender_options = ["All", "M", "F"]
    gender = st.sidebar.selectbox("เลือกเพศผู้ใช้", gender_options)

    age_bins = [1, 18, 25, 35, 45, 50, 56, 100]
    age_labels = ["<18", "18-24", "25-34", "35-44", "45-49", "50-55", "56+"]
    users["age_group"] = pd.cut(users["age"], bins=age_bins, labels=age_labels, right=False)

    age_group_options = ["All"] + age_labels
    selected_age_group = st.sidebar.selectbox("เลือกช่วงอายุผู้ใช้", age_group_options)

    df_filtered = df[df["year"] == year]

    if gender != "All":
        df_filtered = df_filtered[df_filtered["gender"] == gender]

    if selected_age_group != "All":
        user_ids = users[users["age_group"] == selected_age_group]["user_id"]
        df_filtered = df_filtered[df_filtered["user_id"].isin(user_ids)]

    avg_rating = (
        df_filtered.groupby("title")["rating"]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
    )

    if avg_rating.empty:
        st.warning("⚠️ ไม่มีข้อมูลสำหรับเงื่อนไขที่เลือก (ลองเปลี่ยนปี/เพศ/อายุ)")
    else:
        fig, ax = plt.subplots(figsize=(8, 5))
        avg_rating.plot(kind="barh", ax=ax, color="skyblue")
        ax.set_xlabel("Average Rating")
        ax.set_ylabel("Movie Title")
        ax.set_title(
            f"Top {top_n} Movies in {int(year)} "
            f"({'All genders' if gender=='All' else gender}) "
            f"({'All ages' if selected_age_group=='All' else selected_age_group})"
        )
        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.download_button(
            label="📥 Download กราฟ Top Movies",
            data=buf.getvalue(),
            file_name=f"top_movies_{int(year)}.png",
            mime="image/png"
        )

# -------------------------
# Tab 2: Word Cloud
# -------------------------
with tab2:
    st.header("Word Cloud")

    if "genres" in movies.columns:
        text = " ".join(movies["genres"].astype(str))
        label = "Genres"
    else:
        text = " ".join(movies["title"].astype(str))
        label = "Titles"

    wc = WordCloud(width=800, height=400, background_color="white").generate(text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

    buf_wc = io.BytesIO()
    fig.savefig(buf_wc, format="png")
    st.download_button(
        label=f"📥 Download Word Cloud ({label})",
        data=buf_wc.getvalue(),
        file_name=f"wordcloud_{label.lower()}.png",
        mime="image/png"
    )

# -------------------------
# Tab 4: Recommendation System
# -------------------------
with tab4:
    st.header("🤖 Movie Recommendation System")

    user_ids = df["user_id"].unique()
    selected_user = st.selectbox("เลือก User ID", user_ids)

    user_movies = df[df["user_id"] == selected_user]["movie_id"].unique()
    avg_ratings_all = df.groupby("movie_id")["rating"].mean()
    not_watched = set(df["movie_id"].unique()) - set(user_movies)

    # ✅ ใช้ list() ไม่ใช่ set
    recommendations = avg_ratings_all.loc[list(not_watched)].sort_values(ascending=False).head(10)
    rec_movies = movies.set_index("movie_id").loc[recommendations.index]

    st.subheader(f"🎯 แนะนำหนังสำหรับ User {selected_user}")
    st.table(rec_movies[["title"]].assign(average_rating=recommendations.values))

    buf_rec = io.BytesIO()
    rec_movies_out = rec_movies[["title"]].assign(average_rating=recommendations.values)
    rec_movies_out.to_csv(buf_rec, index=False)
    st.download_button(
        label="📥 Download Recommendations (CSV)",
        data=buf_rec.getvalue(),
        file_name=f"recommendations_user_{selected_user}.csv",
        mime="text/csv"
    )

# -------------------------
# Tab 5: Q&A System
# -------------------------
with tab5:
    st.header("💬อันดับหนังยอดนิยม")

    question = st.text_input("พิมพ์คำถาม เช่น 'Top 5 movies in 1995 by females under 25'")

    if question:
        year_match = re.search(r"(\d{4})", question)
        year = int(year_match.group(1)) if year_match else None

        n_match = re.search(r"top\s*(\d+)", question, re.IGNORECASE)
        top_n = int(n_match.group(1)) if n_match else 5

        gender = "All"
        if "female" in question.lower() or "ผู้หญิง" in question:
            gender = "F"
        elif "male" in question.lower() or "ผู้ชาย" in question:
            gender = "M"

        age_limit = None
        if "under" in question.lower():
            age_match = re.search(r"under\s*(\d+)", question.lower())
            if age_match:
                age_limit = int(age_match.group(1))

        df_q = df.copy()
        if year:
            df_q = df_q[df_q["year"] == year]
        if gender != "All":
            df_q = df_q[df_q["gender"] == gender]
        if age_limit:
            df_q = df_q[df_q["age"] < age_limit]

        result = (
            df_q.groupby("title")["rating"]
            .mean()
            .sort_values(ascending=False)
            .head(top_n)
        )

        if result.empty:
            st.warning("⚠️ ไม่มีข้อมูลสำหรับเงื่อนไขที่ถาม")
        else:
            st.subheader("🔎 คำตอบ")
            st.write(result)

# -------------------------
# Tab 6: Predict Rating
# -------------------------
with tab6:
    st.header("🔮 Predict Rating (ทำนายคะแนนที่ User จะให้หนัง)")

    df_ml = df[["user_id", "movie_id", "rating", "age"]].copy()
    df_ml["gender_num"] = df["gender"].map({"M": 0, "F": 1})

    X = df_ml[["user_id", "movie_id", "age", "gender_num"]]
    y = df_ml["rating"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)

    user_ids = users["user_id"].unique()
    selected_user = st.selectbox("เลือก User ID", user_ids, key="pred_user")
    movie_ids = movies["movie_id"].unique()
    selected_movie = st.selectbox("เลือก Movie ID", movie_ids, key="pred_movie")

    user_info = users[users["user_id"] == selected_user].iloc[0]
    age = user_info["age"]
    gender_num = 0 if user_info["gender"] == "M" else 1

    X_new = pd.DataFrame([[selected_user, selected_movie, age, gender_num]],
                         columns=["user_id", "movie_id", "age", "gender_num"])
    predicted_rating = model.predict(X_new)[0]

    st.subheader(f"⭐ คาดว่า User {selected_user} จะให้ {predicted_rating:.2f} ดาว กับหนัง {selected_movie}")