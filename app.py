import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(
    page_title="Dr.J의 부동산", 
    page_icon="🏠",
    layout="centered"
)

# 2. UI 디자인 및 카드 레이아웃 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    
    /* 전체 배경에 이미지 적용: sharpkbju-bot/kb-realestate-app 저장소 bg.jpg */
    .stApp {
        background-image: url("https://raw.githubusercontent.com/sharpkbju-bot/kb-realestate-app/main/bg.jpg"); 
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    html, body, [class*="css"] { font-family: 'Noto+Sans+KR', sans-serif; }

    /* 타이틀 영역 */
    .title-container { width: 100%; padding: 30px 0 15px 0; text-align: center; }
    .brand-name { color: #006400; font-size: clamp(30px, 10vw, 45px); font-weight: 900; font-family: 'Arial Black'; letter-spacing: -2px; }
    .brand-suffix { color: #FF4500; font-size: clamp(16px, 5vw, 24px); font-weight: 900; }

    /* 입력 섹션 카드 & 그림자 */
    div[data-testid="stVerticalBlock"] > div:has(div[data-baseweb="select"]) {
        background: rgba(255, 255, 255, 0.88);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    div[data-baseweb="select"] * { font-weight: 900 !important; font-size: 16px !important; }
    div[data-baseweb="select"] input { caret-color: transparent !important; }
    label[data-testid="stWidgetLabel"] p { font-weight: 900 !important; font-size: 17px !important; color: #333; }

    /* 정보 카드 & 그림자 */
    .content-card {
        background: rgba(255, 255, 255, 0.88);
        border-radius: 18px; 
        padding: 25px; 
        text-align: center; 
        margin-bottom: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .summary-label { color: #555; font-size: 14px; font-weight: 700; margin-bottom: 5px; }
    .summary-date { color: #800080; font-size: 11px; margin-bottom: 10px; font-weight: 700; } /* 진한 퍼플 */

    /* 랭킹 섹션 큰 카드 & 그림자 */
    .ranking-container {
        background: rgba(255, 255, 255, 0.88);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        margin-top: 10px;
        margin-bottom: 30px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    /* [핵심 수정] 개별 순위 카드 그림자 효과 강화 */
    .rank-card {
        background-color: rgba(253, 253, 253, 0.8); /* 배경 투명도 살짝 낮춤 */
        padding: 12px 15px; 
        border-radius: 12px;
        margin-bottom: 10px; 
        display: flex; 
        align-items: center; 
        justify-content: space-between;
        
        /* 그림자 효과 강화 */
        box-shadow: 0 8px 15px rgba(0,0,0,0.1); 
        border: 1px solid rgba(0,0,0,0.03); /* 아주 옅은 테두리 추가 */
        transition: transform 0.2s ease; /* 마우스 오버 효과를 위한 준비 */
    }

    /* 마우스 오버 시 효과 (선택사항, 디자인 포인트) */
    .rank-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    }
    
    .rank-info { display: flex; align-items: center; gap: 10px; color: #333 !important; }
    .rank-num { font-weight: 900; font-size: 16px; }
    .rank-name { font-weight: 700; font-size: 16px; color: #333 !important; }
    .rank-val { font-weight: 900; font-size: 15px; }
    
    .rank-m { border-left: 6px solid #FF4500; }
    .rank-m .rank-num { color: #FF4500; }
    .rank-m .rank-val { color: #e74c3c; }
    
    .rank-j { border-left: 6px solid #000080; }
    .rank-j .rank-num { color: #000080; }
    .rank-j .rank-val { color: #000080; }

    .chart-title {
        font-size: 19px; font-weight: 800; margin: 10px 0 15px 0;
        padding-left: 5px;
        color: #006400; /* 진한 그린 */
    }

    /* 버튼 스타일 */
    div.stButton { text-align: center; margin: 40px 0; display: flex; justify-content: center; }
    div.stButton > button {
        background: linear-gradient(135deg, #424242, #212121) !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 0 40px !important;
        height: 54px !important;
        font-weight: 900 !important;
        font-size: 16px !important;
        border: none !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2) !important;
    }

    /* 종료 화면 */
    .exit-wrapper {
        position: fixed; top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        width: 100%; text-align: center; z-index: 9999;
        background: rgba(255, 255, 255, 0.95);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.2);
    }
    .exit-msg { color: #006400; font-weight: 900; font-size: 32px; margin-top: 20px; }
    .exit-credit { color: #888; font-size: 18px; margin-top: 10px; }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ... (show_title, load_data 함수는 변경 없음)

def main():
    # ... (종료 화면 로직은 변경 없음)
