import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os

# 1. 페이지 설정
st.set_page_config(page_title="Dr.J의 부동산", page_icon="🏠", layout="centered")

# 세션 상태 초기화 및 종료 로직
if "is_exit" not in st.session_state:
    st.session_state.is_exit = False

if st.session_state.is_exit:
    st.markdown("""
        <style>
        .stApp { background-color: white !important; background-image: none !important; }
        .exit-wrapper { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 100%; text-align: center; }
        header { visibility: hidden; }
        </style>
        <div class="exit-wrapper">
            <h1 style="color: #006400; font-weight: 900;">Dr.J의 부동산</h1>
            <h2 style="color: #006400; font-weight: 900;">모두 부자됩시다.</h2>
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

    .brand-name { color: #006400; font-size: 35px; font-weight: 900; }
    .brand-suffix { color: #FF4500; font-size: 20px; font-weight: 900; }

    /* 탭 디자인: 탭명 글자 크기 15px 유지 */
    .stTabs [data-baseweb="tab-list"] { width: 100%; background-color: rgba(255,255,255,0.4); border-radius: 12px 12px 0 0; }
    .stTabs [data-baseweb="tab"] { flex: 1; height: 60px; background-color: rgba(255,255,255,0.8); }
    .stTabs [data-baseweb="tab"] div p { font-size: 15px !important; font-weight: 900 !important; color: #1a1a1a; }
    .stTabs [aria-selected="true"] { background-color: #006400 !important; }
    .stTabs [aria-selected="true"] div p { color: #ffffff !important; }

    /* 선택 박스 내 날짜 글자색(퍼플) 및 Bold */
    div[data-baseweb="select"] div[data-testid="stMarkdownContainer"] p,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {
        color: #4B0082 !important; font-weight: 900 !important; font-size: 18px !important;
    }

    /* 시황 카드 스타일 */
    .stat-card { padding: 15px; border-radius: 12px; margin: 10px 0; display: flex; flex-direction: column; align-items: center; font-weight: 900; font-size: 16px; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .m-card { border-left: 10px solid #FF4500; color: #D32F2F; }
    .j-card { border-left: 10px solid #01579B; color: #01579B; border: 3px solid #FF4500; }

    /* 그래프 터치 차단 */
    .stPlotlyChart { pointer-events: none !important; user-select: none !important; }

    .chart-title { font-size: 18px; font-weight: 900; color: #ffffff; background: #2c3e50; border-radius: 8px; text-align: center; padding: 10px; margin: 20px 0; }
    
    /* 종료 버튼 스타일 */
    div.stButton > button {
        width: 100% !important; height: 55px !important; border-radius: 15px !important;
        font-weight: 900 !important; font-size: 18px !important; color: #FFD700 !important;
        background: linear-gradient(135deg, #444444, #111111) !important;
        border: 2px solid #FFD700 !important;
    }
    header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df_m = pd.read_csv('maemae.csv', encoding='cp949')
        df_j = pd.read_csv('jeonse.csv', encoding='cp949')
    except:
        df_m = pd.read_csv('maemae.csv', encoding='utf-8')
        df_j = pd.read_csv('jeonse.csv', encoding='utf-8')
    for col in df_m.columns:
        if col != '날짜': df_m[col] = pd.to_numeric(df_m[col], errors='coerce').fillna(0)
    for col in df_j.columns:
        if col != '날짜': df_j[col] = pd.to_numeric(df_j[col], errors='coerce').fillna(0)
    return df_m, df_j

def main():
    st.markdown('<div style="text-align:center; padding: 20px;"><span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span></div>', unsafe_allow_html=True)
    
    df_maemae, df_jeonse = load_data()
    date_list = sorted(df_maemae['날짜'].unique().tolist())
    region_list = sorted([col for col in df_maemae.columns if col != '날짜'])

    tab1, tab2, tab3 = st.tabs(["📊 지역분석", "🌡️ 시장온도", "🏆 랭킹TOP"])

    with tab1:
        sel_date = st.selectbox("📅 기준 날짜 선택", date_list, index=len(date_list)-1)
        sel_regions = st.multiselect("🔍 비교 지역 선택", region_list, default=[region_list[0]] if region_list else [])
        
        if sel_regions:
            # --- 시황 카드 출력 로직 복구 ---
            for region in sel_regions:
                m_val = df_maemae[df_maemae['날짜'] == sel_date][region].values[0]
                j_val = df_jeonse[df_jeonse['날짜'] == sel_date][region].values[0]

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f'<div class="stat-card m-card"><div>{region} 매매</div><div style="font-size:24px;">{m_val:+.2f}%</div></div>', unsafe_allow_html=True)
                with col2:
                    # 전세 카드는 강조 테두리 포함
                    st.markdown(f'<div class="stat-card j-card"><div>{region} 전세</div><div style="font-size:24px;">{j_val:+.2f}%</div><div style="color:#FF4500; font-size:12px;">🔥 누적TOP</div></div>', unsafe_allow_html=True)

            # --- 그래프 출력 ---
            curr_idx = date_list.index(sel_date)
            start_idx = max(0, curr_idx - 7)
            graph_font = dict(size=14, color="#6F4E37", family="Noto Sans KR") # 브라운 텍스트

            st.markdown('<div class="chart-title">📈 매매 증감 추이 (최근 8주)</div>', unsafe_allow_html=True)
            sub_m = df_maemae.iloc[start_idx : curr_idx + 1][['날짜'] + sel_regions]
            fig_m = px.line(sub_m, x='날짜', y=sel_regions, markers=True)
            fig_m.update_traces(line_color='#006400', line_width=4) # 다크 그린 선
            fig_m.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=graph_font, hovermode=False)
            st.plotly_chart(fig_m, use_container_width=True, config={'staticPlot': True})

            st.markdown('<div class="chart-title">📉 전세 증감 추이 (최근 8주)</div>', unsafe_allow_html=True)
            sub_j = df_jeonse.iloc[start_idx : curr_idx + 1][['날짜'] + sel_regions]
            fig_j = px.line(sub_j, x='날짜', y=sel_regions, markers=True)
            fig_j.update_traces(line_color='#006400', line_width=4)
            fig_j.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=graph_font, hovermode=False)
            st.plotly_chart(fig_j, use_container_width=True, config={'staticPlot': True})

    # 탭 2, 3 로직 생략 (기존 유지)
    
    # 종료 버튼을 페이지 최하단에 배치
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚪 앱 종료", key="exit_btn", use_container_width=True):
        st.session_state.is_exit = True
        st.rerun()

if __name__ == "__main__":
    main()
