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

    /* 타이틀 디자인 */
    .brand-name { color: #006400; font-size: 35px; font-weight: 900; }
    .brand-suffix { color: #FF4500; font-size: 20px; font-weight: 900; }

    /* 상단 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] { width: 100%; background-color: rgba(255,255,255,0.4); border-radius: 12px 12px 0 0; }
    .stTabs [data-baseweb="tab"] { flex: 1; height: 60px; background-color: rgba(255,255,255,0.8); }
    .stTabs [data-baseweb="tab"] div p { font-size: 18px; font-weight: 900; color: #1a1a1a; }
    .stTabs [aria-selected="true"] { background-color: #006400 !important; }
    .stTabs [aria-selected="true"] div p { color: #ffffff !important; }

    /* ★ 선택 박스 가독성 해결 핵심 섹션 ★ */
    /* 1. 박스 배경색 강제 지정 */
    div[data-baseweb="select"] > div:first-child {
        background-color: #f0f2f6 !important; 
        border: 1px solid #cccccc !important;
        border-radius: 10px !important;
        min-height: 48px !important;
        display: flex !important;
        align-items: center !important;
    }
    
    /* 2. 글자색을 아주 짙은 퍼플로 고정 (안보임 현상 방지) */
    div[data-baseweb="select"] div[data-testid="stMarkdownContainer"] p,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {
        color: #4B0082 !important; 
        font-weight: 900 !important;
        font-size: 18px !important;
        line-height: 1.2 !important;
    }

    /* 위젯 레이블 볼드 */
    label[data-testid="stWidgetLabel"] p { font-weight: 900 !important; font-size: 16px !important; color: #222222 !important; }

    /* 그래프 터치 방지 */
    .stPlotlyChart { pointer-events: none !important; user-select: none !important; }

    /* 섹션 타이틀 및 카드 */
    .chart-title { font-size: 18px; font-weight: 900; color: #ffffff; background: #2c3e50; border-radius: 8px; text-align: center; padding: 10px; margin: 20px 0; }
    .rank-card { padding: 10px 15px; border-radius: 12px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between; font-weight: 900; font-size: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
    .m-weekly { background: linear-gradient(135deg, #FFEFBA, #FFFFFF); border-left: 8px solid #FF4500; color: #D32F2F; }
    .j-weekly { background: linear-gradient(135deg, #E0F7FA, #FFFFFF); border-left: 8px solid #01579B; color: #01579B; }
    
    /* 종료 버튼 */
    div.stButton > button {
        width: 100% !important; height: 50px !important; border-radius: 12px !important;
        font-weight: 900 !important; font-size: 17px !important; color: #FFD700 !important;
        background: linear-gradient(135deg, #555555, #222222) !important;
        border: 2px solid #FFD700 !important; margin-top: 30px !important;
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
        if col != '날짜':
            df_m[col] = pd.to_numeric(df_m[col], errors='coerce').fillna(0)
    for col in df_j.columns:
        if col != '날짜':
            df_j[col] = pd.to_numeric(df_j[col], errors='coerce').fillna(0)
    return df_m, df_j

def main():
    st.markdown('<div style="text-align:center; padding: 20px;"><span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span></div>', unsafe_allow_html=True)
    
    df_maemae, df_jeonse = load_data()
    date_list = sorted(df_maemae['날짜'].unique().tolist())
    region_list = sorted([col for col in df_maemae.columns if col != '날짜'])

    tab1, tab2, tab3 = st.tabs(["📊 지역분석", "🌡️ 시장온도", "🏆 랭킹TOP"])

    with tab1:
        sel_date = st.selectbox("📅 기준 날짜 선택", date_list, index=len(date_list)-1, key="tab1_date")
        sel_regions = st.multiselect("🔍 비교 지역 선택", region_list, default=[region_list[0]] if region_list else [])
        
        if sel_regions:
            curr_idx = date_list.index(sel_date)
            start_idx = max(0, curr_idx - 7)
            
            st.markdown('<div class="chart-title">📈 매매 증감 추이 (최근 8주)</div>', unsafe_allow_html=True)
            sub_m = df_maemae.iloc[start_idx : curr_idx + 1][['날짜'] + sel_regions]
            fig_m = px.line(sub_m, x='날짜', y=sel_regions, markers=True)
            fig_m.update_traces(line_width=6, marker=dict(size=10))
            fig_m.update_layout(height=350, font=dict(size=13, weight=900), hovermode=False)
            st.plotly_chart(fig_m, use_container_width=True, config={'staticPlot': True})

            st.markdown('<div class="chart-title">📉 전세 증감 추이 (최근 8주)</div>', unsafe_allow_html=True)
            sub_j = df_jeonse.iloc[start_idx : curr_idx + 1][['날짜'] + sel_regions]
            fig_j = px.line(sub_j, x='날짜', y=sel_regions, markers=True)
            fig_j.update_traces(line_width=6, marker=dict(size=10))
            fig_j.update_layout(height=350, font=dict(size=13, weight=900), hovermode=False)
            st.plotly_chart(fig_j, use_container_width=True, config={'staticPlot': True})

    with tab2:
        st.markdown('<div class="chart-title">🌡️ 시장 온도계 (8주 합산)</div>', unsafe_allow_html=True)
        m_sum = df_maemae.iloc[max(0, len(date_list)-8):].drop(columns=['날짜']).sum()
        j_sum = df_jeonse.iloc[max(0, len(date_list)-8):].drop(columns=['날짜']).sum()
        heat_df = pd.DataFrame({'매매합계': m_sum, '전세합계': j_sum}).sort_values(by='매매합계', ascending=False)
        st.dataframe(heat_df.style.background_gradient(cmap='RdYlBu_r').format("{:+.2f}%"), use_container_width=True, height=500)

    with tab3:
        sel_date_rank = st.selectbox("📅 랭킹 기준일 선택", date_list, index=len(date_list)-1, key="tab3_date")
        target_row_m = df_maemae[df_maemae['날짜'] == sel_date_rank].drop(columns=['날짜'])
        target_row_j = df_jeonse[df_jeonse['날짜'] == sel_date_rank].drop(columns=['날짜'])

        st.markdown('<div class="chart-title" style="background:#e67e22;">🔥 주간 상승 지역 TOP 10</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<p style="font-weight:900; text-align:center; color:#D32F2F; font-size:16px;">[매매 주간]</p>', unsafe_allow_html=True)
            if not target_row_m.empty:
                m_w = target_row_m.iloc[0].sort_values(ascending=False).head(10)
                for i, (n, v) in enumerate(m_w.items()):
                    if v > 0: st.markdown(f'<div class="rank-card m-weekly"><span>{i+1}. {n}</span><span>+{v:.2f}</span></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<p style="font-weight:900; text-align:center; color:#01579B; font-size:16px;">[전세 주간]</p>', unsafe_allow_html=True)
            if not target_row_j.empty:
                j_w = target_row_j.iloc[0].sort_values(ascending=False).head(10)
                for i, (n, v) in enumerate(j_w.items()):
                    if v > 0: st.markdown(f'<div class="rank-card j-weekly"><span>{i+1}. {n}</span><span>+{v:.2f}</span></div>', unsafe_allow_html=True)

    if st.button("🚪 안전하게 앱 종료하기", key="exit_trigger", use_container_width=True):
        st.session_state.is_exit = True
        st.rerun()

if __name__ == "__main__":
    main()
