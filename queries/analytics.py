# 🎬 Mini Netflix Clone Pro – Movie Analytics Platform

## 📌 Overview
**Mini Netflix Clone Pro** คือระบบวิเคราะห์ข้อมูลภาพยนตร์ที่สร้างขึ้นด้วย  
**PostgreSQL + Python + Streamlit** เพื่อจำลองระบบคล้าย Netflix  

🔹 Features:
- เก็บข้อมูลผู้ใช้ (Users), ภาพยนตร์ (Movies), นักแสดง (Actors), ผู้กำกับ (Directors), แนวหนัง (Genres), การให้คะแนน (Ratings), และประวัติการรับชม (WatchHistory)  
- ออกแบบฐานข้อมูลให้มีความสัมพันธ์แบบ One-to-Many และ Many-to-Many  
- SQL Queries เพื่อดึง Insight ที่น่าสนใจ เช่น  
  - Top 10 Movies โดยเฉลี่ยคะแนนสูงสุด  
  - ผู้ใช้ที่ให้คะแนนมากที่สุด  
  - ค่าเฉลี่ยคะแนนตามปีที่หนังออกฉาย  
  - การให้คะแนนแยกตามเพศและอาชีพผู้ใช้  

---

## 🗄 ER Diagram
![ER Diagram](images/er_diagram.png)

Schema หลัก:
- `users` ↔ `ratings` ↔ `movies`
- `movies` ↔ `movie_actor` ↔ `actors`
- `movies` ↔ `directors`
- `movies` ↔ `genres`
- `users` ↔ `watch_history` ↔ `movies`

---

## 📝 Example SQL Queries

### 🎥 Top 10 Movies by Average Rating
```sql
SELECT m.title, ROUND(AVG(r.rating), 2) AS avg_rating, COUNT(r.rating) AS total_reviews
FROM ratings r
JOIN movies m ON r.movie_id = m.movie_id
GROUP BY m.title
HAVING COUNT(r.rating) > 50
ORDER BY avg_rating DESC
LIMIT 10;
