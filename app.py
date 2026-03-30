import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os

# 1. 페이지 설정
st.set_page_config(
    page_title="Dr.J의 부동산", 
    page_icon="🏠",
    layout="centered"
)

# 세션 상태 초기화 및 종료 로직
if "is_exit" not in st.session_state:
    st.session_state.is_exit = False

if st.session_state.is_exit:
    st.markdown("""
        <style>
        .stApp { background-color: white !important; background-image: none !important; }
        .exit-wrapper { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 100%; text-align: center; z-index: 1000; }
        .exit-logo-font { font-family: 'Noto Sans KR', sans-serif; font-weight: 900; line-height: 1.2; margin-bottom: 15px; }
        .exit-logo-drj { color: #006400; font-size: 50px; }
        .exit-logo-bds { color: #FF4500; font-size: 28px; }
        .exit-wishes { font-size: 20px !important; font-weight: 700; color: #333333; margin-bottom: 10px; }
        .exit-msg { font-size: 16px; color: #666; }
        header { visibility: hidden; }
        </style>
        <div class="exit-wrapper">
            <div class="exit-logo-font">
                <span class="exit-logo-drj">Dr.J</span><span class="exit-logo-bds">의 부동산</span>
            </div>
            <h2 class="exit-wishes">모두 부자됩시다.</h2>
            <p class="exit-msg">with by 70억 자산가 SY.LEE</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# 배경 이미지 주입
def set_bg_from_local(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <style>
            .stApp {{ background-image: url("data:image/jpg;base64,{encoded_string}"); background-size: cover; background-attachment: fixed; background-position: center; }}
            </style>
        """, unsafe_allow_html=True)

set_bg_from_local('bg.jpg')

# UI 디자인 및 스타일 설정
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; color: #000000; }

    /* 메인 타이틀 테두리 복원 */
    .brand-container { 
        text-align: center; 
        padding: 20px; 
        border: 2px solid #006400; 
        border-radius: 15px; 
        background-color: rgba(255,255,255,0.6);
        margin-bottom: 20px;
    }
    .brand-name { color: #006400; font-size: 35px; font-weight: 900; }
    .brand-suffix { color: #FF4500; font-size: 20px; font-weight: 900; }

    /* ★ 탭 메뉴 크기 및 테두리 완벽 복원 ★ */
    .stTabs [data-baseweb="tab-list"] { 
        width: 100% !important; 
        background-color: rgba(255,255,255,0.4) !important; 
        border-radius: 12px 12px 0 0 !important; 
        border: 2px solid #2c3e50 !important;
        padding: 2px !important;
        gap: 0px !important;
    }
    .stTabs [data-baseweb="tab"] { 
        flex: 1 !important; 
        height: 65px !important; 
        background-color: rgba(255,255,255,0.8) !important; 
        border-right: 1px solid #ddd !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    .stTabs [data-baseweb="tab"] div p { 
        font-size: 16px !important; 
        font-weight: 900 !important; 
        color: #1a1a1a !important; 
    }
    .stTabs [aria-selected="true"] { 
        background-color: #006400 !important; 
    }
    .stTabs [aria-selected="true"] div p { 
        color: #ffffff !important; 
    }

    /* ★ 드롭다운 날짜 텍스트 BOLD 처리 복원 ★ */
    div[data-baseweb="select"] > div:first-child {
        background-color: #f0f2f6 !important; 
        border: 2px solid #4B0082 !important; 
        border-radius: 10px !important; 
        min-height: 48px !important;
    }
    
    /* 선택된 텍스트 및 옵션 텍스트 모두 두껍게 고정 */
    div[data-baseweb="select"] span, 
    div[data-baseweb="select"] div[data-testid="stMarkdownContainer"] p,
    div[data-baseweb="select"] div {
        color: #4B0082 !important; 
        font-weight: 900 !important; 
        font-size: 18px !important;
    }
    
    div[data-baseweb="select"] input {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: 900 !important;
    }

    label[data-testid="stWidgetLabel"] p { font-weight: 900 !important; font-size: 16px !important; color: #222222 !important; }

    /* 카드 및 기타 스타일 유지 */
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 69, 0, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(255, 69, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 69, 0, 0); }
    }
    .highlight-card { animation: pulse 2s infinite; border: 4px solid #FF4500 !important; }

    .stat-card { 
        padding: 15px; border-radius: 12px; margin: 10px 0; display: flex; flex-direction: column; align-items: center; 
        font-weight: 900; font-size: 16px; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 1px solid #cccccc;
    }
    .m-card { border-left: 10px solid #FF4500; border-right: 2px solid #FF4500; border-top: 2px solid #FF4500; border-bottom: 2px solid #FF4500; color: #D32F2F; }
    .j-card { border-left: 10px solid #01579B; border-right: 2px solid #01579B; border-top: 2px solid #01579B; border-bottom: 2px solid #01579B; color: #01579B; }

    .chart-title { 
        font-size: 18px; font-weight: 900; color: #ffffff; background: #2c3e50; border-radius: 8px; 
        text-align: center; padding: 10px; margin: 20px 0; border: 2px solid #FFD700;
    }
    
    div.stButton > button {
        width: 100% !important; height: 55px !important; border-radius: 12px !important;
        font-weight: 900 !important; font-size: 18px !important; color: #FFD700 !important;
        background: linear-gradient(135deg, #444444, #111111) !important;
        border: 3px solid #FFD700 !important;
    }

    header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    def read_csv_safe(file):
        try: return pd.read_csv(file, encoding='cp949')
        except UnicodeDecodeError: return pd.read_csv(file, encoding='utf-8')
    df_m = read_csv_safe('maemae.csv')
    df_j = read_csv_safe('jeonse.csv')
    for col in df_m.columns:
        if col != '날짜': df_m[col] = pd.to_numeric(df_m[col], errors='coerce').fillna(0)
    for col in df_j.columns:
        if col != '날짜': df_j[col] = pd.to_numeric(df_j[col], errors='coerce').fillna(0)
    return df_m, df_j

def main():
    st.markdown('<div class="brand-container"><span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span></div>', unsafe_allow_html=True)
    df_maemae, df_jeonse = load_data()
    date_list = sorted(df_maemae['날짜'].unique().tolist())
    region_list = sorted([col for col in df_maemae.columns if col != '날짜'])
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["📊 지역 분석", "🌡️ 시장 온도", "🏆 누적 랭킹 TOP 10"])

    with tab1:
        sel_date = st.selectbox("📅 기준 날짜 선택", date_list, index=len(date_list)-1, key="tab1_date")
        sel_regions = st.multiselect("🔍 비교 지역 선택", region_list, default=[region_list[0]] if region_list else [])
        if sel_regions:
            curr_idx = date_list.index(sel_date)
            for region in sel_regions:
                m_val = df_maemae[df_maemae['날짜'] == sel_date][region].values[0]
                j_val = df_jeonse[df_jeonse['날짜'] == sel_date][region].values[0]
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f'<div class="stat-card m-card"><div>{region} 매매 증감</div><div style="font-size:24px;">{m_val:+.2f}%</div></div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div class="stat-card j-card"><div>{region} 전세 증감</div><div style="font-size:24px;">{j_val:+.2f}%</div></div>', unsafe_allow_html=True)
            
            # 차트 부분 생략 (기존 코드 유지)
            st.markdown('<div class="chart-title">📈 매매 증감 추이 (최근 8주)</div>', unsafe_allow_html=True)
            # ... (차트 생성 로직)

    # 나머지 탭(tab2, tab3) 및 종료 버튼 로직은 기존 파일과 동일하게 유지
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚪 안전하게 앱 종료하기", key="exit_trigger", use_container_width=True):
        st.session_state.is_exit = True
        st.rerun()

if __name__ == "__main__":
    main()
