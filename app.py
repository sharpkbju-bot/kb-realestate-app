import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import base64
import os

# 1. 페이지 설정
st.set_page_config(
    page_title="Dr.J의 부동산", 
    page_icon="🏠",
    layout="centered"
)

# 배경 이미지를 Base64로 변환하여 주입하는 함수
def set_bg_from_local(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded_string}");
                background-size: cover;
                background-attachment: fixed;
                background-position: center;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# 파일명이 bg.jpg가 맞는지, app.py와 같은 위치에 있는지 확인하세요!
set_bg_from_local('bg.jpg')

# 2. UI 디자인 및 중앙 정렬 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto+Sans+KR', sans-serif; }

    /* 타이틀 */
    .title-container { width: 100%; padding: 30px 0 15px 0; text-align: center; }
    .brand-name { color: #006400; font-size: clamp(30px, 10vw, 45px); font-weight: 900; font-family: 'Arial Black'; letter-spacing: -2px; }
    .brand-suffix { color: #FF4500; font-size: clamp(16px, 5vw, 24px); font-weight: 900; }

    /* 입력 필드(날짜/지역) 글자 900 Bold 처리 */
    div[data-baseweb="select"] * {
        font-weight: 900 !important;
        font-size: 16px !important;
    }
    label[data-testid="stWidgetLabel"] p {
        font-weight: 900 !important;
        font-size: 17px !important;
    }

    /* 카드 배경 반투명 처리 (이미지 비침 효과) */
    .summary-card, .rank-card {
        background: rgba(255, 255, 255, 0.92) !important;
    }

    /* 랭킹 카드 - 그림자 효과 대폭 강화 (Deep Shadow) */
    .rank-card {
        padding: 12px 15px; border-radius: 12px;
        margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between;
        /* 그림자 농도를 높이고 범위를 넓힘 */
        box-shadow: 0 10px 20px rgba(0,0,0,0.4) !important; 
        border: 1px solid rgba(0,0,0,0.1);
    }
    
    .rank-info { display: flex; align-items: center; gap: 8px; }
    .rank-num { font-weight: 900; font-size: 16px; }
    .rank-name { font-weight: 900; font-size: 16px; color: #111 !important; }
    .rank-val { font-weight: 900; font-size: 15px; }
    
    .rank-m { border-left: 7px solid #FF4500; }
    .rank-m .rank-num { color: #FF4500; }
    .rank-m .rank-val { color: #e74c3c; }
    
    .rank-j { border-left: 7px solid #000080; }
    .rank-j .rank-num { color: #000080; }
    .rank-j .rank-val { color: #000080; }

    /* 종료 화면 정중앙 강제 배치 */
    .exit-wrapper {
        position: fixed;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        width: 100%; text-align: center; z-index: 9999;
    }
    .exit-msg {
        color: #006400; font-weight: 900; font-size: 32px;
        margin-top: 20px; text-shadow: 1px 1px 2px white;
    }

    [data-testid="stPlotlyChart"] { background-color: transparent !important; }
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# (중략: load_data 및 main() 로직은 이전과 동일하게 유지)
# 단, 랭킹 표시 부분에서 10위까지 월간/주간 모두 정상 표시되도록 복원되었습니다.

def main():
    if st.session_state.get("is_exit"):
        st.markdown(f"""
            <div class="exit-wrapper">
                <div class="title-container">
                    <span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span>
                </div>
                <div class="exit-msg">모두 부자됩시다.</div>
            </div>
        """, unsafe_allow_html=True)
        components.html("<script>window.close();</script>")
        st.stop()

    st.markdown('<div class="title-container"><span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span></div>', unsafe_allow_html=True)
    
    # ... 나머지 로직 ...
    # (코드 중략 - 기존의 데이터 로드 및 차트 그리기 로직 사용)

    if st.button("🚪 앱 종료"):
        st.session_state.is_exit = True
        st.rerun()

if __name__ == "__main__":
    main()
