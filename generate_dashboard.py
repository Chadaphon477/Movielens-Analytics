import os
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt


# เตรียมโฟลเดอร์ images

os.makedirs("images", exist_ok=True)


# เชื่อมต่อ PostgreSQL

conn = psycopg2.connect(
    dbname="movie_analytics",   
    user="postgres",            
    password="123456",        
    host="localhost",
    port="5432"
)


# 1) Average Rating by Year

query1 = """
SELECT m.release_year, ROUND(AVG(r.rating), 2) AS avg_rating
FROM ratings r
JOIN movies m ON r.movie_id = m.movie_id
GROUP BY m.release_year
ORDER BY m.release_year;
"""

df_year = pd.read_sql(query1, conn)

plt.figure(figsize=(10,5))
plt.plot(df_year["release_year"], df_year["avg_rating"], marker="o")
plt.title("Average Movie Rating by Year")
plt.xlabel("Year")
plt.ylabel("Average Rating")
plt.grid(True)
plt.savefig("images/dashboard_ratings_by_year.png")
plt.close()


# 2) Top 10 Movies by Rating

query2 = """
SELECT m.title, ROUND(AVG(r.rating),2) AS avg_rating, COUNT(r.rating) AS total_reviews
FROM ratings r
JOIN movies m ON r.movie_id = m.movie_id
GROUP BY m.title
HAVING COUNT(r.rating) > 50
ORDER BY avg_rating DESC
LIMIT 10;
"""

df_top = pd.read_sql(query2, conn)

plt.figure(figsize=(10,6))
plt.barh(df_top["title"], df_top["avg_rating"], color="skyblue")
plt.gca().invert_yaxis()
plt.title("Top 10 Movies by Average Rating")
plt.xlabel("Average Rating")
plt.savefig("images/dashboard_top_movies.png")
plt.close()


# 3) Ratings by Gender

query3 = """
SELECT u.gender, ROUND(AVG(r.rating),2) AS avg_rating
FROM ratings r
JOIN users u ON r.user_id = u.user_id
GROUP BY u.gender;
"""

df_gender = pd.read_sql(query3, conn)

plt.figure(figsize=(6,6))
plt.bar(df_gender["gender"], df_gender["avg_rating"], color=["pink","lightblue"])
plt.title("Average Ratings by Gender")
plt.ylabel("Average Rating")
plt.savefig("images/dashboard_ratings_by_gender.png")
plt.close()


