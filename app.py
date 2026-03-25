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

# 2. UI 디자인 및 레이아웃 최적화 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto+Sans+KR', sans-serif; }

    /* 타이틀 */
    .title-container { padding: 30px 0 15px 0; text-align: center; }
    .brand-name { color: #006400; font-size: clamp(30px, 10vw, 45px); font-weight: 900; font-family: 'Arial Black'; letter-spacing: -2px; }
    .brand-suffix { color: #FF4500; font-size: clamp(16px, 5vw, 24px); font-weight: 900; }

    /* 매매/전세 증감 카드 스타일 */
    .summary-card {
        background: #ffffff; border-radius: 18px; padding: 20px; 
        text-align: center; margin-bottom: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.07);
        border: 1px solid #f0f0f0;
    }
    .summary-label { color: #666; font-size: 13px; font-weight: 700; margin-bottom: 5px; }
    .summary-date { color: #999; font-size: 11px; margin-bottom: 8px; }

    /* 랭킹 카드 스타일 */
    .rank-card {
        background-color: #ffffff; padding: 12px 15px; border-radius: 12px;
        margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .rank-info { display: flex; align-items: center; gap: 8px; color: #333 !important; }
    .rank-num { font-weight: 900; font-size: 16px; }
    .rank-name { font-weight: 700; font-size: 16px; color: #333 !important; }
    .rank-val { font-weight: 900; font-size: 15px; }
    
    .rank-m { border-left: 6px solid #FF4500; }
    .rank-m .rank-num { color: #FF4500; }
    .rank-m .rank-val { color: #e74c3c; }
    
    .rank-j { border-left: 6px solid #000080; }
    .rank-j .rank-num { color: #000080; }
    .rank-j .rank-val { color: #000080; }

    .chart-title {
        font-size: 18px; font-weight: 800; margin: 35px 0 15px 0;
        padding-left: 12px;
    }

    /* 종료 버튼 중앙 정렬 레이아웃 */
    .exit-wrapper {
        display: flex;
        justify-content: center;
        width: 100%;
        margin: 50px 0;
    }

    /* 종료 버튼 스타일 (그레이 그라데이션) */
    .stButton > button {
        background: linear-gradient(135deg, #757575, #424242) !important;
        color: white !important;
        border-radius: 25px !important;
        width: 180px !important;
        height: 54px !important;
        font-weight: 900 !important;
        font-size: 16px !important;
        border: none !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
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
    # 종료 화면 (짙은 그레이, 한 줄 고정)
    if "is_exit" in st.session_state:
        st.markdown("""
            <div style='display:flex; justify-content:center; align-items:center; height:70vh;'>
                <h2 style='color:#424242; font-weight:900; white-space:nowrap; letter-spacing:-1px;'>모두 부자됩시다.</h2>
            </div>
        """, unsafe_allow_html=True)
        components.html("<script>window.close();</script>")
        st.stop()

    df_maemae, df_jeonse = load_data()
    date_list = sorted(df_maemae['날짜'].unique().tolist())
    region_list = sorted([col for col in df_maemae.columns if col != '날짜'])

    # 1. 날짜 및 지역 선택 필드 (상단 고정)
    sel_date = st.selectbox("📅 날짜 선택", date_list, index=len(date_list)-1)
    sel_region = st.selectbox("🔍 지역 검색 및 선택", options=["지역을 선택하세요."] + region_list, index=0)

    # 지역 선택 시 포커스 해제 (키보드 닫기)
    if sel_region != "지역을 선택하세요.":
        components.html("<script>window.parent.document.activeElement.blur();</script>", height=0)

    # 2. [신규 요청] 선택된 지역의 증감 카드 (필드 바로 아래 배치)
    if sel_region != "지역을 선택하세요.":
        st.markdown(f"<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
        m_val = df_maemae.loc[df_maemae['날짜'] == sel_date, sel_region].values[0]
        j_val = df_jeonse.loc[df_jeonse['날짜'] == sel_date, sel_region].values[0]
        
        m_color = "#e74c3c" if m_val > 0 else "#000080" if m_val < 0 else "#333"
        j_color = "#e74c3c" if j_val > 0 else "#000080" if j_val < 0 else "#333"

        st.markdown(f'''
            <div class="summary-card">
                <div class="summary-label">📍 {sel_region} 전주 대비 매매 증감</div>
                <div class="summary-date">기준: {sel_date}</div>
                <div style="color:{m_color}; font-size:28px; font-weight:900;">{m_val:+.2f}%</div>
            </div>
            <div class="summary-card">
                <div class="summary-label">📍 {sel_region} 전주 대비 전세 증감</div>
                <div class="summary-date">기준: {sel_date}</div>
                <div style="color:{j_color}; font-size:28px; font-weight:900;">{j_val:+.2f}%</div>
            </div>
        ''', unsafe_allow_html=True)

    # 3. 매매/전세 랭킹 섹션
    curr_idx = date_list.index(sel_date)
    
    # [매매 순위]
    st.markdown('<div class="chart-title" style="color:#FF69B4; border-left:6px solid #FF69B4;">🔥 주간 매매 상승 TOP 10</div>', unsafe_allow_html=True)
    m_row = df_maemae[df_maemae['날짜'] == sel_date].drop(columns=['날짜']).iloc[0]
    top_mw = m_row[m_row > 0].sort_values(ascending=False).head(10)
    for i, (name, val) in enumerate(top_mw.items()):
        st.markdown(f'<div class="rank-card rank-m"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    # [전세 순위]
    st.markdown('<div class="chart-title" style="color:#4169E1; border-left:6px solid #4169E1;">💧 주간 전세 상승 TOP 10</div>', unsafe_allow_html=True)
    j_row = df_jeonse[df_jeonse['날짜'] == sel_date].drop(columns=['날짜']).iloc[0]
    top_jw = j_row[j_row > 0].sort_values(ascending=False).head(10)
    for i, (name, val) in enumerate(top_jw.items()):
        st.markdown(f'<div class="rank-card rank-j"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    # 4. 상세 그래프 (하단 배치)
    if sel_region != "지역을 선택하세요.":
        st.markdown("<hr>", unsafe_allow_html=True)
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

        draw_chart(df_maemae, '#e74c3c', f'📈 {sel_region} 매매 트렌드')
        draw_chart(df_jeonse, '#000080', f'📉 {sel_region} 전세 트렌드')

    # 5. 종료 버튼 (정중앙 이동)
    st.markdown("<div class='exit-wrapper'>", unsafe_allow_html=True)
    if st.button("🚪 앱 종료"):
        st.session_state.is_exit = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
