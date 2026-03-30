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

    .brand-name { color: #006400; font-size: 35px; font-weight: 900; }
    .brand-suffix { color: #FF4500; font-size: 20px; font-weight: 900; }

    /* 탭 디자인 */
    .stTabs [data-baseweb="tab-list"] { width: 100%; background-color: rgba(255,255,255,0.4); border-radius: 12px; }
    .stTabs [data-baseweb="tab"] { flex: 1; height: 70px; background-color: rgba(255,255,255,0.8); }
    .stTabs [data-baseweb="tab"] div p { font-size: 19px; font-weight: 900; color: #1a1a1a; }
    .stTabs [aria-selected="true"] { background-color: #006400 !important; }
    .stTabs [aria-selected="true"] div p { color: #ffffff !important; }

    /* 위젯 라벨 볼드 */
    label[data-testid="stWidgetLabel"] p { font-weight: 900 !important; font-size: 18px !important; color: #111111 !important; }
    
    /* 선택 박스 스타일 */
    div[data-baseweb="select"] > div:first-child {
        background-color: #f0f2f6 !important; 
        border: 2px solid #999999 !important;
        border-radius: 10px !important;
        min-height: 50px !important;
    }
    div[data-baseweb="select"] span, div[data-baseweb="select"] div {
        color: #4B0082 !important; font-weight: 900 !important; font-size: 18px !important;
    }

    /* ★ 앱 종료 버튼 커스텀 (네이비 배경 + 밝은 핑크 글씨) ★ */
    .stButton > button {
        width: 100% !important; 
        height: 65px !important; 
        border-radius: 15px !important;
        font-weight: 900 !important; 
        font-size: 22px !important; 
        color: #FF69B4 !important; /* 밝은 핑크 (Hot Pink) */
        background-color: #000080 !important; /* 진한 네이비 (Navy) */
        border: 3px solid #FF69B4 !important; /* 테두리도 핑크로 강조 */
        margin-top: 40px !important;
        box-shadow: 0 4px 15px rgba(0,0,128,0.3) !important;
    }
    .stButton > button:hover {
        color: #ffffff !important;
        background-color: #0000CD !important;
    }

    .chart-title { font-size: 18px; font-weight: 900; color: #ffffff; background: #2c3e50; border-radius: 8px; text-align: center; padding: 10px; margin: 20px 0 10px 0; }
    
    .highlight-card { animation: pulse 2s infinite; border: 3px solid #FF4500 !important; }
    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(255, 69, 0, 0.7); } 70% { box-shadow: 0 0 0 15px rgba(255, 69, 0, 0); } 100% { box-shadow: 0 0 0 0 rgba(255, 69, 0, 0); } }

    .stat-card { padding: 15px; border-radius: 12px; margin: 10px 0; display: flex; flex-direction: column; align-items: center; font-weight: 900; font-size: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); background: white; }
    .m-card { border-left: 10px solid #FF4500; color: #D32F2F; }
    .j-card { border-left: 10px solid #01579B; color: #01579B; }

    .rank-card { padding: 10px 12px; border-radius: 12px; margin-bottom: 6px; display: flex; align-items: center; justify-content: space-between; font-weight: 900; font-size: 14px; }
    .m-weekly { background: linear-gradient(135deg, #FFEFBA, #FFFFFF); border-left: 6px solid #FF4500; color: #D32F2F; }
    .j-weekly { background: linear-gradient(135deg, #E0F7FA, #FFFFFF); border-left: 6px solid #01579B; color: #01579B; }
    .m-accum { background: linear-gradient(135deg, #FFF9C4, #FFFFFF); border-left: 6px solid #FBC02D; color: #7F6000; }  
    .j-accum { background: linear-gradient(135deg, #E8F5E9, #FFFFFF); border-left: 6px solid #2E7D32; color: #1B5E20; }

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
    st.markdown('<div style="text-align:center; padding: 15px;"><span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span></div>', unsafe_allow_html=True)
    
    df_maemae, df_jeonse = load_data()
    date_list = sorted(df_maemae['날짜'].unique().tolist())
    region_list = sorted([col for col in df_maemae.columns if col != '날짜'])

    tab1, tab2, tab3 = st.tabs(["📊 지역분석", "🌡️ 시장온도", "🏆 랭킹 TOP 10"])

    with tab1:
        # [삭제됨] 폼 형식을 제거하여 선택 즉시 반영되도록 복구
        sel_date = st.selectbox("📅 기준 날짜 선택", date_list, index=len(date_list)-1, key="tab1_date")
        sel_regions = st.multiselect("🔍 비교 지역 선택", region_list, default=[region_list[0]] if region_list else [])
        
        if sel_regions:
            curr_idx = date_list.index(sel_date)
            m_accum_top = df_maemae.iloc[max(0, curr_idx-7) : curr_idx+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10).index.tolist()
            j_accum_top = df_jeonse.iloc[max(0, curr_idx-7) : curr_idx+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10).index.tolist()

            for region in sel_regions:
                m_val = df_maemae[df_maemae['날짜'] == sel_date][region].values[0]
                j_val = df_jeonse[df_jeonse['날짜'] == sel_date][region].values[0]
                is_m_hot, is_j_hot = region in m_accum_top, region in j_accum_top

                col1, col2 = st.columns(2)
                with col1:
                    m_class = "stat-card m-card highlight-card" if is_m_hot else "stat-card m-card"
                    st.markdown(f'<div class="{m_class}"><div>{region} 매매</div><div style="font-size:20px;">{m_val:+.2f}%</div>{"<small>🔥누적TOP</small>" if is_m_hot else ""}</div>', unsafe_allow_html=True)
                with col2:
                    j_class = "stat-card j-card highlight-card" if is_j_hot else "stat-card j-card"
                    st.markdown(f'<div class="{j_class}"><div>{region} 전세</div><div style="font-size:20px;">{j_val:+.2f}%</div>{"<small>🔥누적TOP</small>" if is_j_hot else ""}</div>', unsafe_allow_html=True)

            start_idx = max(0, curr_idx - 7)
            graph_font = dict(size=14, color="#000080", family="Noto Sans KR")
            
            st.markdown('<div class="chart-title">📈 매매 증감 추이 (최근 8주)</div>', unsafe_allow_html=True)
            sub_m = df_maemae.iloc[start_idx : curr_idx + 1][['날짜'] + sel_regions]
            fig_m = px.line(sub_m, x='날짜', y=sel_regions, markers=True)
            fig_m.update_traces(line_width=6, marker=dict(size=10))
            fig_m.update_layout(height=320, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=graph_font, hovermode=False, xaxis=dict(tickfont=dict(weight='bold')), yaxis=dict(tickfont=dict(weight='bold')))
            st.plotly_chart(fig_m, use_container_width=True, config={'staticPlot': True})

            st.markdown('<div class="chart-title">📉 전세 증감 추이 (최근 8주)</div>', unsafe_allow_html=True)
            sub_j = df_jeonse.iloc[start_idx : curr_idx + 1][['날짜'] + sel_regions]
            fig_j = px.line(sub_j, x='날짜', y=sel_regions, markers=True)
            fig_j.update_traces(line_width=6, marker=dict(size=10))
            fig_j.update_layout(height=320, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=graph_font, hovermode=False, xaxis=dict(tickfont=dict(weight='bold')), yaxis=dict(tickfont=dict(weight='bold')))
            st.plotly_chart(fig_j, use_container_width=True, config={'staticPlot': True})

    with tab2:
        st.markdown('<div class="chart-title">🌡️ 시장 온도계 (8주 합산)</div>', unsafe_allow_html=True)
        m_sum = df_maemae.iloc[max(0, len(date_list)-8):].drop(columns=['날짜']).sum()
        j_sum = df_jeonse.iloc[max(0, len(date_list)-8):].drop(columns=['날짜']).sum()
        heat_df = pd.DataFrame({'지역명': m_sum.index, '매매 합계': m_sum.values, '전세 합계': j_sum.values}).sort_values(by='매매 합계', ascending=False)
        
        st.dataframe(
            heat_df.style.background_gradient(cmap='RdYlBu_r', subset=['매매 합계', '전세 합계'])
            .format({'매매 합계': '{:+.2f}%', '전세 합계': '{:+.2f}%'})
            .set_properties(**{'font-weight': '900', 'color': '#000000', 'font-size': '16px'}),
            use_container_width=True, height=550, hide_index=True
        )

    with tab3:
        sel_date_rank = st.selectbox("📅 랭킹 기준일 선택", date_list, index=len(date_list)-1, key="tab3_date")
        curr_idx_rank = date_list.index(sel_date_rank)
        
        st.markdown('<div class="chart-title" style="background:#e67e22;">🔥 주간 상승 지역 TOP 10</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<p style="text-align:center; font-weight:900; color:#D32F2F;">[매매 주간]</p>', unsafe_allow_html=True)
            m_w = df_maemae[df_maemae['날짜'] == sel_date_rank].drop(columns=['날짜']).iloc[0].sort_values(ascending=False).head(10)
            for n, v in m_w.items():
                if v > 0: st.markdown(f'<div class="rank-card m-weekly"><span>{n}</span><span>+{v:.2f}</span></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<p style="text-align:center; font-weight:900; color:#01579B;">[전세 주간]</p>', unsafe_allow_html=True)
            j_w = df_jeonse[df_jeonse['날짜'] == sel_date_rank].drop(columns=['날짜']).iloc[0].sort_values(ascending=False).head(10)
            for n, v in j_w.items():
                if v > 0: st.markdown(f'<div class="rank-card j-weekly"><span>{n}</span><span>+{v:.2f}</span></div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-title" style="background:#f1c40f; color:#000;">📊 8주 누적 상승 TOP 10</div>', unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<p style="text-align:center; font-weight:900; color:#7F6000;">[매매 누적]</p>', unsafe_allow_html=True)
            m_8 = df_maemae.iloc[max(0, curr_idx_rank-7) : curr_idx_rank+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10)
            for n, v in m_8.items():
                if v > 0: st.markdown(f'<div class="rank-card m-accum"><span>{n}</span><span>+{v:.2f}%</span></div>', unsafe_allow_html=True)
        with c4:
            st.markdown('<p style="text-align:center; font-weight:900; color:#1B5E20;">[전세 누적]</p>', unsafe_allow_html=True)
            j_8 = df_jeonse.iloc[max(0, curr_idx_rank-7) : curr_idx_rank+1].drop(columns=['날짜']).sum().sort_values(ascending=False).head(10)
            for n, v in j_8.items():
                if v > 0: st.markdown(f'<div class="rank-card j-accum"><span>{n}</span><span>+{v:.2f}%</span></div>', unsafe_allow_html=True)

    # 하단 종료 버튼
    if st.button("🚪 앱 종료", key="exit_trigger"):
        st.session_state.is_exit = True
        st.rerun()

if __name__ == "__main__":
    main()
