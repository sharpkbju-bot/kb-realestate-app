import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(
    page_title="Dr.J의 부동산", 
    page_icon="🏠",
    layout="centered"
)

# 2. 고도화된 레이아웃 및 디자인 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto+Sans+KR', sans-serif; }

    /* 타이틀 설정 */
    .title-container { padding: 40px 0 20px 0; text-align: center; }
    .brand-name { color: #006400; font-size: clamp(35px, 12vw, 50px); font-weight: 900; font-family: 'Arial Black'; letter-spacing: -2px; }
    .brand-suffix { color: #FF4500; font-size: clamp(18px, 5vw, 28px); font-weight: 900; }

    /* 랭킹 카드 */
    .rank-card {
        background-color: #fffaf0; padding: 10px 12px; border-radius: 10px;
        margin-bottom: 8px; border-left: 5px solid #FF4500;
        display: flex; align-items: center; justify-content: space-between;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .rank-info { display: flex; align-items: center; gap: 8px; }
    .rank-num { font-weight: 900; color: #FF4500; min-width: 20px; font-size: 14px; }
    .rank-name { font-weight: 700; color: #333; font-size: 13px; }
    .rank-val { font-weight: 900; color: #e74c3c; font-size: 13px; }

    /* 매매/전세 카드 간격 분리 (중요!) */
    .metric-box {
        background: white; border: 1px solid #f0f0f0; border-radius: 15px;
        padding: 18px; text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        margin: 10px 5px !important; /* 카드 좌우/상하 간격 확보 */
    }

    /* 하단 버튼 가로 나란히 배치 강제 (모바일 포함) */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 10px !important;
    }
    
    .stButton > button {
        border-radius: 12px; font-weight: bold; height: 50px;
        border: none; font-size: 16px; width: 100% !important;
    }
    
    /* 초기화 버튼 (연한 파랑) */
    div[data-testid="column"]:nth-child(1) button {
        background-color: #D1E9F6 !important; color: #004080 !important;
    }
    /* 종료 버튼 (연한 그린) */
    div[data-testid="column"]:nth-child(2) button {
        background-color: #D1F2D1 !important; color: #006400 !important;
    }

    .chart-title {
        font-size: 17px; font-weight: 800; margin: 30px 0 10px 0;
        color: #C71585; border-left: 6px solid #C71585; padding-left: 12px;
    }

    header {visibility: hidden;}
    .static-chart { pointer-events: none !important; }
    </style>
    
    <div class="title-container">
        <span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span>
    </div>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df_m = pd.read_csv('maemae.csv', encoding='cp949')
        df_j = pd.read_csv('jeonse.csv', encoding='cp949')
    except:
        df_m = pd.read_csv('maemae.csv', encoding='utf-8')
        df_j = pd.read_csv('jeonse.csv', encoding='utf-8')
    
    common_cols = ['날짜'] + sorted(list(set(df_m.columns) & set(df_j.columns) - {'날짜'}))
    df_m, df_j = df_m[common_cols], df_j[common_cols]
    
    for col in [c for c in df_m.columns if c != '날짜']:
        df_m[col] = pd.to_numeric(df_m[col], errors='coerce').fillna(0)
        df_j[col] = pd.to_numeric(df_j[col], errors='coerce').fillna(0)
    
    df_m['날짜'] = df_m['날짜'].astype(str)
    return df_m, df_j

def main():
    if "is_exit" in st.session_state:
        st.markdown("<div style='text-align:center; padding:50px;'><h2>앱이 종료되었습니다.</h2></div>", unsafe_allow_html=True)
        st.stop()

    df_maemae, df_jeonse = load_data()
    date_list = sorted(df_maemae['날짜'].unique().tolist())
    region_list = sorted([col for col in df_maemae.columns if col != '날짜'])

    # 초기화 카운터
    if "reset_count" not in st.session_state:
        st.session_state.reset_count = 0

    # 입력란
    c_date, c_search = st.columns([1, 1.5])
    with c_date:
        sel_date = st.selectbox("📅 날짜", date_list, index=len(date_list)-1, key=f"d_{st.session_state.reset_count}")
    with c_search:
        sel_region = st.selectbox("🔍 지역 선택", options=["지역을 선택하세요."] + region_list, index=0, key=f"r_{st.session_state.reset_count}")

    # 1. 랭킹 (주간/월간)
    r1, r2 = st.columns(2)
    with r1:
        st.markdown('<div class="chart-title">🔥 주간 상승 TOP 10</div>', unsafe_allow_html=True)
        w_row = df_maemae[df_maemae['날짜'] == sel_date].drop(columns=['날짜']).iloc[0]
        top_w = w_row[w_row > 0].sort_values(ascending=False).head(10)
        for i, (name, val) in enumerate(top_w.items()):
            st.markdown(f'<div class="rank-card"><div class="rank-info"><span class="rank-num">{i+1}</span><span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)
    with r2:
        st.markdown('<div class="chart-title">📅 월간 상승 TOP 10</div>', unsafe_allow_html=True)
        curr_idx = date_list.index(sel_date)
        if curr_idx >= 3:
            m_sum = df_maemae.iloc[curr_idx-3 : curr_idx+1].drop(columns=['날짜']).sum()
            top_m = m_sum[m_sum > 0].sort_values(ascending=False).head(10)
            for i, (name, val) in enumerate(top_m.items()):
                st.markdown(f'<div class="rank-card"><div class="rank-info"><span class="rank-num">{i+1}</span><span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)
        else:
            st.info("데이터 부족")

    # 2. 상세 정보 (매매/전세 카드 간격 수정)
    if sel_region != "지역을 선택하세요.":
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"#### 📍 {sel_region} 시황", unsafe_allow_html=True)
        m_val = df_maemae.loc[df_maemae['날짜'] == sel_date, sel_region].values[0]
        j_val = df_jeonse.loc[df_jeonse['날짜'] == sel_date, sel_region].values[0]

        m_color = "#e74c3c" if m_val > 0 else "#000080" if m_val < 0 else "#333"
        j_color = "#e74c3c" if j_val > 0 else "#000080" if j_val < 0 else "#333"

        # 카드 2개를 컬럼에 담되 마진을 주어 붙지 않게 함
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.markdown(f'<div class="metric-box"><div style="color:#4B0082; font-weight:800; font-size:14px;">전주 대비 매매 증감</div><div style="color:{m_color}; font-size:24px; font-weight:900;">{m_val:+.2f}%</div></div>', unsafe_allow_html=True)
        with m_col2:
            st.markdown(f'<div class="metric-box"><div style="color:#4B0082; font-weight:800; font-size:14px;">전주 대비 전세 증감</div><div style="color:{j_color}; font-size:24px; font-weight:900;">{j_val:+.2f}%</div></div>', unsafe_allow_html=True)

        # 4주 그래프
        start_idx = max(0, curr_idx - 3)
        st.markdown('<div class="chart-title">📈 매매 지수 트렌드 (4주)</div>', unsafe_allow_html=True)
        fig_m = px.line(df_maemae.iloc[start_idx:curr_idx+1], x='날짜', y=sel_region, markers=True)
        fig_m.update_traces(line_color='#e74c3c', line_width=4, marker=dict(size=10, color='white', line=dict(width=2, color='#e74c3c')))
        fig_m.update_layout(height=220, margin=dict(l=10,r=10,t=10,b=10), xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True), hovermode=False)
        st.plotly_chart(fig_m, use_container_width=True, config={'staticPlot': True})

        st.markdown('<div class="chart-title">📉 전세 지수 트렌드 (4주)</div>', unsafe_allow_html=True)
        fig_j = px.line(df_jeonse.iloc[start_idx:curr_idx+1], x='날짜', y=sel_region, markers=True)
        fig_j.update_traces(line_color='#000080', line_width=4, marker=dict(size=10, color='white', line=dict(width=2, color='#000080')))
        fig_j.update_layout(height=220, margin=dict(l=10,r=10,t=10,b=10), xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True), hovermode=False)
        st.plotly_chart(fig_j, use_container_width=True, config={'staticPlot': True})

    # 3. 버튼 영역 (가로 나란히 강제 배치)
    st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
    btn1, btn2 = st.columns(2)
    with btn1:
        if st.button("🔄 초기화"):
            st.session_state.reset_count += 1
            st.rerun()
    with btn2:
        if st.button("🚪 종료"):
            st.session_state.is_exit = True
            st.rerun()

if __name__ == "__main__":
    main()
