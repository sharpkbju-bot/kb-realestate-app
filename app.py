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
        .exit-title { font-size: 30px !important; font-weight: 900; color: #000080; margin-bottom: 10px; }
        .exit-wishes { font-size: 20px !important; font-weight: 700; color: #333333; margin-bottom: 10px; }
        .exit-msg { font-size: 16px; color: #666; }
        header { visibility: hidden; }
        </style>
        <div class="exit-wrapper">
            <h1 class="exit-title">Dr.J의 부동산</h1>
            <h2 class="exit-wishes">모두 부자됩시다.</h2>
            <p class="exit-msg">안전하게 종료되었습니다.</p>
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

    .stTabs [data-baseweb="tab-list"] { width: 100%; background-color: rgba(255,255,255,0.4); border-radius: 12px 12px 0 0; }
    .stTabs [data-baseweb="tab"] { flex: 1; height: 60px; background-color: rgba(255,255,255,0.8); }
    .stTabs [data-baseweb="tab"] div p { font-size: 15px !important; font-weight: 900 !important; color: #1a1a1a; }
    .stTabs [aria-selected="true"] { background-color: #006400 !important; }
    .stTabs [aria-selected="true"] div p { color: #ffffff !important; }

    div[data-baseweb="select"] > div:first-child {
        background-color: #f0f2f6 !important; border: 1px solid #cccccc !important; border-radius: 10px !important; min-height: 48px !important; display: flex !important; align-items: center !important;
    }
    
    div[data-baseweb="select"] div[data-testid="stMarkdownContainer"] p,
    div[data-baseweb="select"] span, div[data-baseweb="select"] div {
        color: #4B0082 !important; font-weight: 900 !important; font-size: 18px !important;
    }

    label[data-testid="stWidgetLabel"] p { font-weight: 900 !important; font-size: 16px !important; color: #222222 !important; }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 69, 0, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(255, 69, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 69, 0, 0); }
    }
    .highlight-card {
        animation: pulse 2s infinite;
        border: 3px solid #FF4500 !important;
    }

    .stat-card { padding: 15px; border-radius: 12px; margin: 10px 0; display: flex; flex-direction: column; align-items: center; font-weight: 900; font-size: 16px; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .m-card { border-left: 10px solid #FF4500; color: #D32F2F; }
    .j-card { border-left: 10px solid #01579B; color: #01579B; }

    .stPlotlyChart { pointer-events: none !important; user-select: none !important; }
    .chart-title { font-size: 18px; font-weight: 900; color: #ffffff; background: #2c3e50; border-radius: 8px; text-align: center; padding: 10px; margin: 20px 0; }
    
    .rank-card { padding: 10px 15px; border-radius: 12px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between; font-weight: 900; font-size: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
    .m-weekly { background: linear-gradient(135deg, #FFEFBA, #FFFFFF); border-left: 8px solid #FF4500; color: #D32F2F; }
    .j-weekly { background: linear-gradient(135deg, #E0F7FA, #FFFFFF); border-left: 8px solid #01579B; color: #01579B; }
    .m-accum { background: linear-gradient(135deg, #FFF9C4, #FFFFFF); border-left: 8px solid #FBC02D; color: #7F6000; }  
    .j-accum { background: linear-gradient(135deg, #E8F5E9, #FFFFFF); border-left: 8px solid #2E7D32; color: #1B5E20; }
    
    div.stButton > button {
        width: 100% !important; height: 55px !important; border-radius: 12px !important;
        font-weight: 900 !important; font-size: 18px !important; color: #FFD700 !important;
        background: linear-gradient(135deg, #444444, #111111) !important;
        border: 2px solid #FFD700 !important;
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
    st.markdown('<div style="text-align:center; padding: 20px;"><span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span></div>', unsafe_allow_html=True)
    df_maemae, df_jeonse = load_data()
    date_list = sorted(df_maemae['날짜'].unique().tolist())
    region_list = sorted([col for col in df_maemae.columns if col != '날짜'])
    tab1, tab2, tab3 = st.tabs(["📊 지역 분석", "🌡️ 시장 온도", "🏆 누적 랭킹 TOP 10"])

    with tab1:
        sel_date = st.selectbox("📅 기준 날짜 선택", date_list, index=len(date_list)-1, key="tab1_date")
        sel_regions = st.multiselect("🔍 비교 지역 선택", region_list, default=[region_list[0]] if region_list else [])
        if sel_regions:
            curr_idx = date_list.index(sel_date)
            m_accum_top = df_maemae.iloc[max(0, curr_idx-7) : curr_idx+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10).index.tolist()
            j_accum_top = df_jeonse.iloc[max(0, curr_idx-7) : curr_idx+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10).index.tolist()
            for region in sel_regions:
                m_val = df_maemae[df_maemae['날짜'] == sel_date][region].values[0]
                j_val = df_jeonse[df_jeonse['날짜'] == sel_date][region].values[0]
                is_m_hot = region in m_accum_top
                is_j_hot = region in j_accum_top
                col1, col2 = st.columns(2)
                with col1:
                    m_class = "stat-card m-card highlight-card" if is_m_hot else "stat-card m-card"
                    st.markdown(f'<div class="{m_class}"><div>{region} 매매</div><div style="font-size:24px;">{m_val:+.2f}%</div></div style="color:#FF4500; font-size:12px;">🔥 누적 TOP</div></div>', unsafe_allow_html=True)
                with col2:
                    j_class = "stat-card j-card highlight-card" if is_j_hot else "stat-card j-card"
                    st.markdown(f'<div class="{j_class}"><div>{region} 전세</div><div style="font-size:24px;">{j_val:+.2f}%</div></div style="color:#FF4500; font-size:12px;">🔥 누적 TOP</div></div>', unsafe_allow_html=True)
            start_idx = max(0, curr_idx - 7)
            custom_colors = px.colors.qualitative.Plotly.copy()
            custom_colors[0] = '#006400'
            st.markdown('<div class="chart-title">📈 매매 증감 추이 (최근 8주)</div>', unsafe_allow_html=True)
            sub_m = df_maemae.iloc[start_idx : curr_idx + 1][['날짜'] + sel_regions]
            fig_m = px.line(sub_m, x='날짜', y=sel_regions, markers=True, color_discrete_sequence=custom_colors)
            fig_m.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#6F4E37"), hovermode=False)
            st.plotly_chart(fig_m, use_container_width=True, config={'staticPlot': True})
            st.markdown('<div class="chart-title">📉 전세 증감 추이 (최근 8주)</div>', unsafe_allow_html=True)
            sub_j = df_jeonse.iloc[start_idx : curr_idx + 1][['날짜'] + sel_regions]
            fig_j = px.line(sub_j, x='날짜', y=sel_regions, markers=True, color_discrete_sequence=custom_colors)
            fig_j.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#6F4E37"), hovermode=False)
            st.plotly_chart(fig_j, use_container_width=True, config={'staticPlot': True})

    with tab2:
        st.markdown('<div class="chart-title">🌡️ 시장 온도계 (8주 합산)</div>', unsafe_allow_html=True)
        m_sum = df_maemae.iloc[-8:].drop(columns=['날짜']).sum()
        j_sum = df_jeonse.iloc[-8:].drop(columns=['날짜']).sum()
        heat_df = pd.DataFrame({'매매합계': m_sum, '전세합계': j_sum}).sort_values(by='매매합계', ascending=False)
        
        # ★ 차트 내부 글자 중앙 정렬 및 Bold 처리 ★
        st.dataframe(
            heat_df.style.background_gradient(cmap='RdYlBu_r')
            .format("{:+.2f}%")
            .set_properties(**{'text-align': 'center', 'font-weight': '900'})
            .set_table_styles([{'selector': 'th', 'props': [('text-align', 'center'), ('font-weight', '900')]}])
            , use_container_width=True, height=500
        )

    with tab3:
        sel_date_rank = st.selectbox("📅 랭킹 기준일 선택", date_list, index=len(date_list)-1, key="tab3_date")
        curr_idx_rank = date_list.index(sel_date_rank)
        st.markdown('<div class="chart-title" style="background:#e67e22;">🔥 주간 상승 지역 TOP 10</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<p style="font-weight:900; text-align:center; color:#D32F2F; font-size:15px;">[매매 주간 상승률]</p>', unsafe_allow_html=True)
            m_w = df_maemae[df_maemae['날짜'] == sel_date_rank].drop(columns=['날짜']).iloc[0].sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(m_w.items()):
                if v > 0: st.markdown(f'<div class="rank-card m-weekly"><span>{i+1}. {n}</span><span>+{v:.2f}</span></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<p style="font-weight:900; text-align:center; color:#01579B; font-size:15px;">[전세 주간 상승률]</p>', unsafe_allow_html=True)
            j_w = df_jeonse[df_jeonse['날짜'] == sel_date_rank].drop(columns=['날짜']).iloc[0].sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(j_w.items()):
                if v > 0: st.markdown(f'<div class="rank-card j-weekly"><span>{i+1}. {n}</span><span>+{v:.2f}</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-title" style="background:#f1c40f; color:#000;">📊 8주 누적 상승 TOP 10</div>', unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<p style="font-weight:900; text-align:center; color:#7F6000; font-size:15px;">[매매 누적 상승률]</p>', unsafe_allow_html=True)
            m_8 = df_maemae.iloc[max(0, curr_idx_rank-7) : curr_idx_rank+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(m_8.items()):
                if v > 0: st.markdown(f'<div class="rank-card m-accum"><span>{i+1}. {n}</span><span>+{v:.2f}%</span></div>', unsafe_allow_html=True)
        with c4:
            st.markdown('<p style="font-weight:900; text-align:center; color:#1B5E20; font-size:15px;">[전세 누적 상승률]</p>', unsafe_allow_html=True)
            j_8 = df_jeonse.iloc[max(0, curr_idx_rank-7) : curr_idx_rank+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10)
            for i, (n, v) in enumerate(j_8.items()):
                if v > 0: st.markdown(f'<div class="rank-card j-accum"><span>{i+1}. {n}</span><span>+{v:.2f}%</span></div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚪 안전하게 앱 종료하기", key="exit_trigger", use_container_width=True):
        st.session_state.is_exit = True
        st.rerun()

if __name__ == "__main__":
    main()
