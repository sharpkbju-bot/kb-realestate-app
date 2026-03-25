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

# 2. 강력한 모바일 가로 배치 및 디자인 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto+Sans+KR', sans-serif; }

    /* 타이틀 */
    .title-container { padding: 30px 0 15px 0; text-align: center; }
    .brand-name { color: #006400; font-size: clamp(30px, 10vw, 45px); font-weight: 900; font-family: 'Arial Black'; letter-spacing: -2px; }
    .brand-suffix { color: #FF4500; font-size: clamp(16px, 5vw, 24px); font-weight: 900; }

    /* 랭킹 카드 */
    .rank-card {
        background-color: #ffffff; padding: 12px 15px; border-radius: 12px;
        margin-bottom: 8px; border-left: 6px solid #FF4500;
        display: flex; align-items: center; justify-content: space-between;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .rank-info { display: flex; align-items: center; gap: 8px; color: #333 !important; }
    .rank-num { font-weight: 900; color: #FF4500; font-size: 16px; }
    .rank-name { font-weight: 700; font-size: 16px; color: #333 !important; }
    .rank-val { font-weight: 900; color: #e74c3c; font-size: 15px; }
    
    /* 전세 랭킹용 카드 색상 차별화 */
    .rank-card-j { border-left: 6px solid #000080; }
    .rank-card-j .rank-num { color: #000080; }
    .rank-card-j .rank-val { color: #000080; }

    /* 섹션 타이틀 */
    .chart-title {
        font-size: 18px; font-weight: 800; margin: 35px 0 15px 0;
        color: #FF69B4; border-left: 6px solid #FF69B4; padding-left: 12px;
    }
    .chart-title-blue { color: #4169E1; border-left: 6px solid #4169E1; }

    /* 핵심: 버튼 가로 배치 강제 고정 */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        justify-content: center !important;
        align-items: center !important;
        gap: 15px !important;
        width: 100% !important;
        flex-wrap: nowrap !important; /* 줄바꿈 절대 방지 */
    }
    
    [data-testid="column"] {
        width: 45% !important; /* 각 버튼이 절반 정도 차지하도록 */
        flex: none !important;
    }

    .stButton > button {
        border-radius: 25px !important;
        height: 52px !important;
        font-weight: 900 !important;
        font-size: 15px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }

    /* 초기화 버튼 (블루 그라데이션) */
    div[data-testid="column"]:nth-child(1) button {
        background: linear-gradient(135deg, #6dd5ed, #2193b0) !important; color: white !important;
    }
    /* 종료 버튼 (오렌지 그라데이션) */
    div[data-testid="column"]:nth-child(2) button {
        background: linear-gradient(135deg, #ff9966, #ff5e62) !important; color: white !important;
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

def display_rankings(df, date, title, is_maemae=True):
    st.markdown(f'<div class="chart-title {"" if is_maemae else "chart-title-blue"}">{title}</div>', unsafe_allow_html=True)
    row = df[df['날짜'] == date].drop(columns=['날짜']).iloc[0]
    top_10 = row[row > 0].sort_values(ascending=False).head(10)
    
    card_class = "rank-card" if is_maemae else "rank-card rank-card-j"
    for i, (name, val) in enumerate(top_10.items()):
        st.markdown(f'<div class="{card_class}"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

def main():
    if "is_exit" in st.session_state:
        st.markdown("<div style='text-align:center; padding:120px 20px;'><h1 style='color:#FF4500; font-size:42px; font-weight:900;'>모두 부자됩시다.</h1></div>", unsafe_allow_html=True)
        components.html("<script>window.close();</script>")
        st.stop()

    df_maemae, df_jeonse = load_data()
    date_list = sorted(df_maemae['날짜'].unique().tolist())
    region_list = sorted([col for col in df_maemae.columns if col != '날짜'])

    if "reset_count" not in st.session_state:
        st.session_state.reset_count = 0

    # 입력부
    sel_date = st.selectbox("📅 날짜 선택", date_list, index=len(date_list)-1, key=f"d_{st.session_state.reset_count}")
    sel_region = st.selectbox("🔍 지역 검색 및 선택", options=["지역을 선택하세요"] + region_list, index=0, key=f"r_{st.session_state.reset_count}")

    # 1. 매매 순위
    display_rankings(df_maemae, sel_date, "🔥 주간 매매 상승 TOP 10", is_maemae=True)
    
    curr_idx = date_list.index(sel_date)
    if curr_idx >= 3:
        m_sum = df_maemae.iloc[curr_idx-3 : curr_idx+1].drop(columns=['날짜']).sum()
        st.markdown('<div class="chart-title">📅 월간 매매 상승 TOP 10</div>', unsafe_allow_html=True)
        top_m = m_sum[m_sum > 0].sort_values(ascending=False).head(10)
        for i, (name, val) in enumerate(top_m.items()):
            st.markdown(f'<div class="rank-card"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    # 2. 전세 순위 (새로 추가)
    display_rankings(df_jeonse, sel_date, "💧 주간 전세 상승 TOP 10", is_maemae=False)
    
    if curr_idx >= 3:
        j_sum = df_jeonse.iloc[curr_idx-3 : curr_idx+1].drop(columns=['날짜']).sum()
        st.markdown('<div class="chart-title chart-title-blue">📅 월간 전세 상승 TOP 10</div>', unsafe_allow_html=True)
        top_j = j_sum[j_sum > 0].sort_values(ascending=False).head(10)
        for i, (name, val) in enumerate(top_j.items()):
            st.markdown(f'<div class="rank-card rank-card-j"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    # 개별 분석 섹션 생략 가능 (기존과 동일하게 작동)
    if sel_region != "지역을 선택하세요":
        st.markdown("<hr>", unsafe_allow_html=True)
        # ... (상세 분석 및 그래프 로직 동일)

    # --- 하단 버튼 (중앙 가로 나란히 강제 고정) ---
    st.markdown("<div style='margin-bottom:60px;'></div>", unsafe_allow_html=True)
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
