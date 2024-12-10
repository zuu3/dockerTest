from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import random
from datetime import datetime

app = FastAPI()

# 1. 날씨 데이터 생성
def generate_weather_data():
    cities = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "수원", "제주", "청주", "춘천"]
    weather_conditions = ["맑음", "구름 많음", "비", "눈", "흐림", "바람"]

    data = []
    for city in cities:
        temperature = round(random.uniform(-5, 35), 1)  # -5도에서 35도 사이
        humidity = random.randint(30, 90)  # 30%에서 90% 사이
        wind_speed = round(random.uniform(0, 15), 1)  # 0 ~ 15m/s
        condition = random.choice(weather_conditions)

        # 날씨 상태 아이콘 매칭
        match condition:
            case "맑음":
                icon = "☀️"
            case "구름 많음":
                icon = "☁️"
            case "비":
                icon = "🌧️"
            case "눈":
                icon = "❄️"
            case "흐림":
                icon = "🌥️"
            case "바람":
                icon = "💨"
            case _:
                icon = "❓"

        data.append({
            "도시": city,
            "온도 (°C)": temperature,
            "습도 (%)": humidity,
            "풍속 (m/s)": wind_speed,
            "날씨": f"{condition} {icon}"  # 날씨 상태와 아이콘 결합
        })

    return pd.DataFrame(data)

# 2. FastAPI 엔드포인트 작성하기
@app.get("/", response_class=HTMLResponse)
async def show_weather():
    df = generate_weather_data()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # HTML 테이블로 변환
    table_html = df.to_html(index=False, escape=False, justify="center", border=1)

    # HTML 페이지 생성
    html_content = f"""
    <html>
        <head>
            <title>대한민국 주요 도시 날씨</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; background-color: #f9f9f9; }}
                table {{ margin: 20px auto; border-collapse: collapse; width: 90%; }}
                th, td {{ padding: 10px; border: 1px solid #ddd; text-align: center; }}
                th {{ background-color: #f4f4f4; color: #333; }}
                td {{ font-size: 14px; }}
                .refresh-btn {{
                    display: inline-block;
                    margin: 20px;
                    padding: 10px 20px;
                    font-size: 16px;
                    color: white;
                    background-color: #007BFF;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    text-decoration: none;
                }}
                .refresh-btn:hover {{
                    background-color: #0056b3;
                }}
                .timestamp {{ font-size: 14px; color: #555; }}
            </style>
        </head>
        <body>
            <h1>대한민국 주요 도시 날씨 정보</h1>
            <p class="timestamp">현재 시간: {current_time}</p>
            <a href="/" class="refresh-btn">새로고침</a>
            {table_html}
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
