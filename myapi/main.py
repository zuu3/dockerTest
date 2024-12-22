from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
import sqlite3
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

app = FastAPI()

# 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect("schedule.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY,
            title TEXT,
            date TEXT,
            description TEXT
        )
    """)
    conn.close()

init_db()

# 메인 페이지: 일정 조회
@app.get("/", response_class=HTMLResponse)
def read_schedule():
    conn = sqlite3.connect("schedule.db")
    schedules = conn.execute("SELECT title, date, description FROM schedule").fetchall()
    conn.close()

    html = "<h1>일정 관리</h1><a href='/add'>일정 추가</a><br><a href='/chart'>가장 많은 일정 보기</a><ul>"
    for title, date, description in schedules:
        html += f"<li>{date} - {title} ({description})</li>"
    html += "</ul>"
    return html

# 일정 추가 페이지
@app.get("/add", response_class=HTMLResponse)
def add_event_page():
    return """
    <h1>일정 추가</h1>
    <form action="/add" method="post">
        제목: <input type="text" name="title"><br>
        날짜: <input type="date" name="date"><br>
        설명: <input type="text" name="description"><br>
        <button type="submit">추가</button>
    </form>
    <a href="/">메인으로</a>
    """

# 일정 추가 처리
@app.post("/add")
def add_event(title: str = Form(...), date: str = Form(...), description: str = Form("")):
    conn = sqlite3.connect("schedule.db")
    conn.execute("INSERT INTO schedule (title, date, description) VALUES (?, ?, ?)", (title, date, description))
    conn.commit()
    conn.close()
    return HTMLResponse("<h1>일정이 추가되었습니다!</h1><a href='/'>메인으로</a>")

# 차트 생성 및 표시
@app.get("/chart")
def show_chart():
    conn = sqlite3.connect("schedule.db")
    data = conn.execute("SELECT date, COUNT(*) as count FROM schedule GROUP BY date ORDER BY count DESC").fetchall()
    conn.close()

    if not data:
        return HTMLResponse("<h1>일정이 없습니다!</h1><a href='/'>메인으로</a>")

    # 데이터 추출
    dates = [row[0] for row in data]
    counts = [row[1] for row in data]

    # 차트 생성
    plt.figure(figsize=(10, 5))
    plt.bar(dates, counts, color='skyblue')
    plt.xlabel("day")
    plt.ylabel("day count")
    plt.title("most day of iljung")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 차트 저장
    chart_path = "schedule_chart.png"
    plt.savefig(chart_path)
    plt.close()

    return FileResponse(chart_path)