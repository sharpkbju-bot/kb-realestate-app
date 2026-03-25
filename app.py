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

# 2. 다크모드 대응 및 모바일 레이아웃 고정 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto+Sans+KR', sans-serif; }

    /* 타이틀 */
    .title-container { padding: 30px 0 15px 0; text-align: center; }
    .brand-name { color: #006400; font-size: clamp(30px, 10vw, 45px); font-weight: 900; font-family: 'Arial Black'; letter-spacing: -2px; }
    .brand-suffix { color: #FF4500; font-size: clamp(16px, 5vw, 24px); font-weight: 900; }

    /* 랭킹 카드 - 배경이 검정일 때도 글자가 보이도록 배경과 글자색 지정 */
    .rank-card {
        background-color: #ffffff; padding: 12px 15px; border-radius: 10px;
        margin-bottom: 8px; border-left: 6px solid #FF4500;
        display: flex; align-items: center; justify-content: space-between;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .rank-info { display: flex; align-items: center; gap: 8px; color: #333333 !important; }
    .rank-num { font-weight: 900; color: #FF4500; font-size: 16px; }
    .rank-name { font-weight: 700; font-size: 16px; color: #333333 !important; }
    .rank-val { font-weight: 900; color: #e74c3c; font-size: 15px; }

    /* 매매/전세 수치 카드 */
    .metric-box {
        background: #ffffff; border: 1px solid #f0f0f0; border-radius: 15px;
        padding: 18px; text-align: center; margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .metric-date { font-size: 12px; color: #666; margin-bottom: 5px; }

    /* 하단 버튼 영역 - 무조건 가로 나란히 */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 10px !important;
    }
    
    .stButton > button {
        border-radius: 12px !important; height: 54px !important;
        font-weight: 900 !important; font-size: 16px !important; border: none !important;
    }
    
    /* 버튼 컬러 */
    div[data-testid="column"]:nth-child(1) button { background-color: #D1E9F6 !important; color: #004080 !important; }
    div[data-testid="column"]:nth-child(2) button { background-color: #D1F2D1 !important; color: #006400 !important; }

    .chart-title {
        font-size: 18px; font-weight: 800; margin: 35px 0 15px 0;
        color: #FF69B4; border-left: 6px solid #FF69B4; padding-left: 12px;
    }

    header {visibility: hidden;}
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
        st.markdown("<div style='text-align:center; padding:50px;'><h1 style='color:#FF4500;'>모두 부자됩시다.</h1></div>", unsafe_allow_html=True)
        components.html("<script>window.close();</script>")
        st.stop()

    df_maemae, df_jeonse = load_data()
    date_list = sorted(df_maemae['날짜'].unique().tolist())
    region_list = sorted([col for col in df_maemae.columns if col != '날짜'])

    if "reset_count" not in st.session_state:
        st.session_state.reset_count = 0

    # 입력 필드
    sel_date = st.selectbox("📅 날짜 선택", date_list, index=len(date_list)-1, key=f"d_{st.session_state.reset_count}")
    sel_region = st.selectbox("🔍 지역 검색 및 선택", options=["지역을 선택하세요"] + region_list, index=0, key=f"r_{st.session_state.reset_count}")

    # 주간 랭킹 (1위 관악구 형식)
    st.markdown('<div class="chart-title">🔥 주간 상승 TOP 10</div>', unsafe_allow_html=True)
    w_row = df_maemae[df_maemae['날짜'] == sel_date].drop(columns=['날짜']).iloc[0]
    top_w = w_row[w_row > 0].sort_values(ascending=False).head(10)
    for i, (name, val) in enumerate(top_w.items()):
        st.markdown(f'<div class="rank-card"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    # 월간 랭킹 (누락 복원 및 1위 형식)
    st.markdown('<div class="chart-title">📅 월간 상승 TOP 10 (4주 누적)</div>', unsafe_allow_html=True)
    curr_idx = date_list.index(sel_date)
    if curr_idx >= 3:
        m_sum = df_maemae.iloc[curr_idx-3 : curr_idx+1].drop(columns=['날짜']).sum()
        top_m = m_sum[m_sum > 0].sort_values(ascending=False).head(10)
        for i, (name, val) in enumerate(top_m.items()):
            st.markdown(f'<div class="rank-card"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    # 개별 분석
    if sel_region != "지역을 선택하세요":
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"#### 📍 {sel_region} 분석", unsafe_allow_html=True)
        
        m_val = df_maemae.loc[df_maemae['날짜'] == sel_date, sel_region].values[0]
        j_val = df_jeonse.loc[df_jeonse['날짜'] == sel_date, sel_region].values[0]
        m_color = "#e74c3c" if m_val > 0 else "#000080" if m_val < 0 else "#333"
        j_color = "#e74c3c" if j_val > 0 else "#000080" if j_val < 0 else "#333"

        st.markdown(f'''
            <div class="metric-box">
                <div class="metric-date">기준: {sel_date}</div>
                <div style="color:#4B0082; font-weight:800; font-size:14px;">매매 증감</div>
                <div style="color:{m_color}; font-size:26px; font-weight:900;">{m_val:+.2f}%</div>
            </div>
            <div class="metric-box">
                <div class="metric-date">기준: {sel_date}</div>
                <div style="color:#4B0082; font-weight:800; font-size:14px;">전세 증감</div>
                <div style="color:{j_color}; font-size:26px; font-weight:900;">{j_val:+.2f}%</div>
            </div>
        ''', unsafe_allow_html=True)

        # 그래프 (그린 포인트)
        start_idx = max(0, curr_idx - 3)
        def draw_chart(df, line_color, title):
            st.markdown(f'<div class="chart-title">{title}</div>', unsafe_allow_html=True)
            sub_df = df.iloc[start_idx : curr_idx + 1]
            fig = px.line(sub_df, x='날짜', y=sel_region, markers=True)
            fig.update_traces(line_color=line_color, line_width=4, marker=dict(size=10, color='white', line=dict(width=2, color=line_color)))
            fig.add_scatter(x=[sel_date], y=[sub_df.loc[sub_df['날짜']==sel_date, sel_region].values[0]], 
                            mode='markers', marker=dict(size=14, color='#00FF00', line=dict(width=3, color='white')), showlegend=False)
            fig.update_layout(height=220, margin=dict(l=10,r=10,t=10,b=10), xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True), hovermode=False)
            st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})

        draw_chart(df_maemae, '#e74c3c', '📈 매매 지수 트렌드 (4주)')
        draw_chart(df_jeonse, '#000080', '📉 전세 지수 트렌드 (4주)')

    # 하단 버튼 (중앙 가로 나란히)
    st.markdown("<div style='margin-top:30px;'></div>", unsafe_allow_html=True)
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        if st.button("🔄 초기화"):
            st.session_state.reset_count += 1
            st.rerun()
    with b_col2:
        if st.button("🚪 종료"):
            st.session_state.is_exit = True
            st.rerun()

if __name__ == "__main__":
    main()
