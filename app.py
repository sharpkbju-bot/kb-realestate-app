import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(
    page_title="Dr.J의 부동산", 
    page_icon="🏠",
    layout="centered"
)

# 2. 모바일 최적화 레이아웃 및 디자인 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto+Sans+KR', sans-serif; }

    /* 타이틀 설정 */
    .title-container { padding: 30px 0 15px 0; text-align: center; }
    .brand-name { color: #006400; font-size: clamp(30px, 10vw, 45px); font-weight: 900; font-family: 'Arial Black'; letter-spacing: -2px; }
    .brand-suffix { color: #FF4500; font-size: clamp(16px, 5vw, 24px); font-weight: 900; }

    /* 입력 필드 레이블 간격 조절 */
    .stSelectbox { margin-bottom: 10px; }

    /* 랭킹 카드 디자인 (세로 배치 최적화) */
    .rank-card {
        background-color: #fffaf0; padding: 12px 15px; border-radius: 10px;
        margin-bottom: 8px; border-left: 6px solid #FF4500;
        display: flex; align-items: center; justify-content: space-between;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .rank-info { display: flex; align-items: center; gap: 10px; }
    .rank-num { font-weight: 900; color: #FF4500; min-width: 25px; font-size: 16px; }
    .rank-name { font-weight: 700; color: #333; font-size: 15px; }
    .rank-val { font-weight: 900; color: #e74c3c; font-size: 15px; }

    /* 매매/전세 지수 카드 (세로 배치로 변경하여 가독성 높임) */
    .metric-box {
        background: white; border: 1px solid #f0f0f0; border-radius: 15px;
        padding: 20px; text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        margin-bottom: 12px;
    }

    /* 하단 버튼 가로 나란히 배치 (강제 고정) */
    .fixed-btn-container {
        display: flex !important;
        flex-direction: row !important;
        gap: 10px !important;
        margin-top: 30px;
        justify-content: center;
    }
    
    .stButton > button {
        border-radius: 12px; font-weight: bold; height: 52px;
        border: none; font-size: 16px; width: 100% !important;
    }
    
    /* 버튼 개별 컬러 */
    div[data-testid="column"]:nth-child(1) button {
        background-color: #D1E9F6 !important; color: #004080 !important;
    }
    div[data-testid="column"]:nth-child(2) button {
        background-color: #D1F2D1 !important; color: #006400 !important;
    }

    .chart-title {
        font-size: 18px; font-weight: 800; margin: 35px 0 15px 0;
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

    if "reset_count" not in st.session_state:
        st.session_state.reset_count = 0

    # --- 입력 필드 세로 배치 (폰에서 안 잘리게 수정) ---
    sel_date = st.selectbox("📅 날짜 선택", date_list, 
                            index=len(date_list)-1, 
                            key=f"date_v_{st.session_state.reset_count}")
    
    sel_region = st.selectbox("🔍 지역 검색 및 선택", 
                              options=["지역을 선택하세요"] + region_list, 
                              index=0, 
                              key=f"region_v_{st.session_state.reset_count}")

    # --- 주간 상승 TOP 10 ---
    st.markdown('<div class="chart-title">🔥 주간 상승 TOP 10</div>', unsafe_allow_html=True)
    w_row = df_maemae[df_maemae['날짜'] == sel_date].drop(columns=['날짜']).iloc[0]
    top_w = w_row[w_row > 0].sort_values(ascending=False).head(10)
    
    if not top_w.empty:
        for i, (name, val) in enumerate(top_w.items()):
            st.markdown(f'<div class="rank-card"><div class="rank-info"><span class="rank-num">{i+1}</span><span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    # --- 월간 상승 TOP 10 ---
    st.markdown('<div class="chart-title">📅 월간 상승 TOP 10 (4주 누적)</div>', unsafe_allow_html=True)
    curr_idx = date_list.index(sel_date)
    if curr_idx >= 3:
        m_sum = df_maemae.iloc[curr_idx-3 : curr_idx+1].drop(columns=['날짜']).sum()
        top_m = m_sum[m_sum > 0].sort_values(ascending=False).head(10)
        for i, (name, val) in enumerate(top_m.items()):
            st.markdown(f'<div class="rank-card"><div class="rank-info"><span class="rank-num">{i+1}</span><span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    # --- 개별 지역 상세 시황 (세로 배치) ---
    if sel_region != "지역을 선택하세요":
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"#### 📍 {sel_region} 상세 분석", unsafe_allow_html=True)
        
        m_val = df_maemae.loc[df_maemae['날짜'] == sel_date, sel_region].values[0]
        j_val = df_jeonse.loc[df_jeonse['날짜'] == sel_date, sel_region].values[0]
        m_color = "#e74c3c" if m_val > 0 else "#000080" if m_val < 0 else "#333"
        j_color = "#e74c3c" if j_val > 0 else "#000080" if j_val < 0 else "#333"

        # 카드도 세로로 배치하여 폰에서 가독성 확보
        st.markdown(f'<div class="metric-box"><div style="color:#4B0082; font-weight:800; font-size:14px;">매매 증감</div><div style="color:{m_color}; font-size:26px; font-weight:900;">{m_val:+.2f}%</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-box"><div style="color:#4B0082; font-weight:800; font-size:14px;">전세 증감</div><div style="color:{j_color}; font-size:26px; font-weight:900;">{j_val:+.2f}%</div></div>', unsafe_allow_html=True)

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

    # --- 하단 버튼 (중앙 나란히 배치) ---
    st.markdown("<div style='margin-top:30px;'></div>", unsafe_allow_html=True)
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("🔄 초기화"):
            st.session_state.reset_count += 1
            st.rerun()
    with btn_col2:
        if st.button("🚪 종료"):
            st.session_state.is_exit = True
            st.rerun()

if __name__ == "__main__":
    main()
