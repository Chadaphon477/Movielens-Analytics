import matplotlib.pyplot as plt
import os

# สร้างโฟลเดอร์ images 
os.makedirs("images", exist_ok=True)

def create_placeholder(filename, text):
    fig, ax = plt.subplots(figsize=(6,4))
    ax.set_facecolor("lightgray")
    ax.text(0.5, 0.5, text, fontsize=16, ha="center", va="center", color="black")
    ax.axis("off")
    plt.savefig(filename, bbox_inches="tight")
    plt.close()

# สร้าง mockup ครบ 6 รูป 
create_placeholder("images/home.png", "🏠 Home Screenshot here")
create_placeholder("images/dashboard_top_movies.png", "📊 Top Movies Screenshot here")
create_placeholder("images/wordcloud.png", "☁️ Word Cloud Screenshot here")
create_placeholder("images/recommendation.png", "🤖 Recommendation Screenshot here")
create_placeholder("images/qa.png", "💬 Q&A System Screenshot here")
create_placeholder("images/predict_rating.png", "🔮 Predict Rating Screenshot here")
