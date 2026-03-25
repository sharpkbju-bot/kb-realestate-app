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

# 2. UI 디자인 및 입력 필드 제어 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto+Sans+KR', sans-serif; }

    /* 타이틀 */
    .title-container { padding: 30px 0 15px 0; text-align: center; }
    .brand-name { color: #006400; font-size: clamp(30px, 10vw, 45px); font-weight: 900; font-family: 'Arial Black'; letter-spacing: -2px; }
    .brand-suffix { color: #FF4500; font-size: clamp(16px, 5vw, 24px); font-weight: 900; }

    /* 랭킹 카드 공통 */
    .rank-card {
        background-color: #ffffff; padding: 12px 15px; border-radius: 12px;
        margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .rank-info { display: flex; align-items: center; gap: 8px; color: #333 !important; }
    .rank-num { font-weight: 900; font-size: 16px; }
    .rank-name { font-weight: 700; font-size: 16px; color: #333 !important; }
    .rank-val { font-weight: 900; font-size: 15px; }
    
    /* 매매(빨강), 전세(파랑) 구분 */
    .rank-m { border-left: 6px solid #FF4500; }
    .rank-m .rank-num { color: #FF4500; }
    .rank-m .rank-val { color: #e74c3c; }
    
    .rank-j { border-left: 6px solid #000080; }
    .rank-j .rank-num { color: #000080; }
    .rank-j .rank-val { color: #000080; }

    /* 섹션 타이틀 */
    .chart-title {
        font-size: 18px; font-weight: 800; margin: 35px 0 15px 0;
        padding-left: 12px;
    }

    /* 종료 버튼 전용 레이아웃 (중앙 정렬) */
    .exit-container {
        display: flex; justify-content: center; margin: 40px 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #757575, #424242) !important;
        color: white !important;
        border-radius: 25px !important;
        width: 160px !important;
        height: 50px !important;
        font-weight: 900 !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
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
    # 종료 화면 처리
    if "is_exit" in st.session_state:
        st.markdown("""
            <div style='display:flex; justify-content:center; align-items:center; height:40vh;'>
                <h2 style='color:#424242; font-weight:600; white-space:nowrap;'>모두 부자됩시다.</h2>
            </div>
        """, unsafe_allow_html=True)
        components.html("<script>window.close();</script>")
        st.stop()

    df_maemae, df_jeonse = load_data()
    date_list = sorted(df_maemae['날짜'].unique().tolist())
    region_list = sorted([col for col in df_maemae.columns if col != '날짜'])

    # 1. 입력 필드 (선택 시 포커스 해제 스크립트 포함)
    sel_date = st.selectbox("📅 날짜 선택", date_list, index=len(date_list)-1)
    sel_region = st.selectbox("🔍 지역 검색 및 선택", options=["지역을 선택하세요."] + region_list, index=0)

    # 지역이 선택되면 포커스를 강제로 제거하여 키보드를 닫는 JS
    if sel_region != "지역을 선택하세요.":
        components.html("<script>window.parent.document.activeElement.blur();</script>", height=0)

    # 2. 순위 표시 섹션 (매매 & 전세)
    # [매매 주간/월간]
    st.markdown('<div class="chart-title" style="color:#FF69B4; border-left:6px solid #FF69B4;">🔥 주간 매매 상승 TOP 10</div>', unsafe_allow_html=True)
    m_row = df_maemae[df_maemae['날짜'] == sel_date].drop(columns=['날짜']).iloc[0]
    top_mw = m_row[m_row > 0].sort_values(ascending=False).head(10)
    for i, (name, val) in enumerate(top_mw.items()):
        st.markdown(f'<div class="rank-card rank-m"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    curr_idx = date_list.index(sel_date)
    if curr_idx >= 3:
        st.markdown('<div class="chart-title" style="color:#FF69B4; border-left:6px solid #FF69B4;">📅 월간 매매 상승 TOP 10</div>', unsafe_allow_html=True)
        m_sum = df_maemae.iloc[curr_idx-3 : curr_idx+1].drop(columns=['날짜']).sum()
        top_mm = m_sum[m_sum > 0].sort_values(ascending=False).head(10)
        for i, (name, val) in enumerate(top_mm.items()):
            st.markdown(f'<div class="rank-card rank-m"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    # [전세 주간/월간]
    st.markdown('<div class="chart-title" style="color:#4169E1; border-left:6px solid #4169E1;">💧 주간 전세 상승 TOP 10</div>', unsafe_allow_html=True)
    j_row = df_jeonse[df_jeonse['날짜'] == sel_date].drop(columns=['날짜']).iloc[0]
    top_jw = j_row[j_row > 0].sort_values(ascending=False).head(10)
    for i, (name, val) in enumerate(top_jw.items()):
        st.markdown(f'<div class="rank-card rank-j"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    if curr_idx >= 3:
        st.markdown('<div class="chart-title" style="color:#4169E1; border-left:6px solid #4169E1;">📅 월간 전세 상승 TOP 10</div>', unsafe_allow_html=True)
        j_sum = df_jeonse.iloc[curr_idx-3 : curr_idx+1].drop(columns=['날짜']).sum()
        top_jm = j_sum[j_sum > 0].sort_values(ascending=False).head(10)
        for i, (name, val) in enumerate(top_jm.items()):
            st.markdown(f'<div class="rank-card rank-j"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    # 3. 상세 분석 (그래프 등)
    if sel_region != "지역을 선택하세요.":
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"#### 📍 {sel_region} 분석 ({sel_date})", unsafe_allow_html=True)
        # (기존의 그래프 및 수치 카드 로직 동일 적용)
        m_val = df_maemae.loc[df_maemae['날짜'] == sel_date, sel_region].values[0]
        j_val = df_jeonse.loc[df_jeonse['날짜'] == sel_date, sel_region].values[0]
        
        m_color = "#e74c3c" if m_val > 0 else "#000080" if m_val < 0 else "#333"
        j_color = "#e74c3c" if j_val > 0 else "#000080" if j_val < 0 else "#333"

        st.markdown(f'''
            <div style="background:white; border-radius:15px; padding:20px; text-align:center; margin-bottom:15px; box-shadow:0 4px 10px rgba(0,0,0,0.05);">
                <div style="color:#666; font-size:12px;">전주 대비 매매 증감</div>
                <div style="color:{m_color}; font-size:24px; font-weight:900;">{m_val:+.2f}%</div>
            </div>
            <div style="background:white; border-radius:15px; padding:20px; text-align:center; margin-bottom:15px; box-shadow:0 4px 10px rgba(0,0,0,0.05);">
                <div style="color:#666; font-size:12px;">전주 대비 전세 증감</div>
                <div style="color:{j_color}; font-size:24px; font-weight:900;">{j_val:+.2f}%</div>
            </div>
        ''', unsafe_allow_html=True)

    # 4. 종료 버튼 (중앙 배치)
    st.markdown("<div class='exit-container'>", unsafe_allow_html=True)
    if st.button("🚪 종료"):
        st.session_state.is_exit = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
