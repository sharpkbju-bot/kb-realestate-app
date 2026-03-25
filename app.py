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

# 2. UI 디자인 및 카드 레이아웃 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    
    /* 전체 배경에 이미지 적용 */
    .stApp {
        background-image: url("https://raw.githubusercontent.com/YourGitHubID/YourRepo/main/background.png"); 
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    html, body, [class*="css"] { font-family: 'Noto+Sans+KR', sans-serif; }

    /* 타이틀 */
    .title-container { width: 100%; padding: 30px 0 15px 0; text-align: center; }
    .brand-name { color: #006400; font-size: clamp(30px, 10vw, 45px); font-weight: 900; font-family: 'Arial Black'; letter-spacing: -2px; }
    .brand-suffix { color: #FF4500; font-size: clamp(16px, 5vw, 24px); font-weight: 900; }

    /* 입력 필드 카드화 및 그림자 */
    div[data-testid="stVerticalBlock"] > div:has(div[data-baseweb="select"]) {
        background: rgba(255, 255, 255, 0.85);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    div[data-baseweb="select"] * { font-weight: 900 !important; font-size: 16px !important; }
    div[data-baseweb="select"] input { caret-color: transparent !important; }
    label[data-testid="stWidgetLabel"] p { font-weight: 900 !important; font-size: 17px !important; color: #333; }

    /* 증감/그래프 카드 스타일 및 그림자 */
    .content-card {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 18px; 
        padding: 25px; 
        text-align: center; 
        margin-bottom: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .summary-label { color: #555; font-size: 14px; font-weight: 700; margin-bottom: 5px; }
    .summary-date { color: #800080; font-size: 11px; margin-bottom: 10px; font-weight: 700; } /* 진한 퍼플 */

    /* 랭킹 섹션 카드화 및 그림자 */
    .ranking-container {
        background: rgba(255, 255, 255, 0.85);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-top: 10px;
        margin-bottom: 30px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    .rank-card {
        background-color: rgba(253, 253, 253, 0.7); 
        padding: 12px 15px; 
        border-radius: 12px;
        margin-bottom: 10px; 
        display: flex; 
        align-items: center; 
        justify-content: space-between;
        border: 1px solid #f0f0f0;
    }
    
    .rank-info { display: flex; align-items: center; gap: 10px; color: #333 !important; }
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
        font-size: 19px; font-weight: 800; margin: 10px 0 15px 0;
        padding-left: 5px;
        color: #006400; /* 진한 그린 */
    }

    /* 버튼 스타일 */
    div.stButton { text-align: center; margin: 40px 0; display: flex; justify-content: center; }
    div.stButton > button {
        background: linear-gradient(135deg, #424242, #212121) !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 0 40px !important;
        height: 54px !important;
        font-weight: 900 !important;
        font-size: 16px !important;
        border: none !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2) !important;
    }

    /* 종료 화면 */
    .exit-wrapper {
        position: fixed; top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        width: 100%; text-align: center; z-index: 9999;
        background: rgba(255, 255, 255, 0.9);
        padding: 40px;
        border-radius: 20px;
    }
    .exit-msg { color: #006400; font-weight: 900; font-size: 32px; margin-top: 20px; }
    .exit-credit { color: #888; font-size: 18px; margin-top: 10px; }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def show_title():
    st.markdown("""
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
    if st.session_state.get("is_exit"):
        st.markdown(f"""
            <div class="exit-wrapper">
                <div class="title-container">
                    <span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span>
                </div>
                <div class="exit-msg">모두 부자됩시다.</div>
                <div class="exit-credit">Created by Ju Kyung Bae</div>
            </div>
        """, unsafe_allow_html=True)
        components.html("<script>window.close();</script>")
        st.stop()

    show_title()

    df_maemae, df_jeonse = load_data()
    date_list = sorted(df_maemae['날짜'].unique().tolist())
    region_list = sorted([col for col in df_maemae.columns if col != '날짜'])

    sel_date = st.selectbox("📅 날짜 선택", date_list, index=len(date_list)-1)
    sel_region = st.selectbox("🔍 지역 검색 및 선택", options=["지역을 입력하세요."] + region_list, index=0)

    if sel_region != "지역을 입력하세요.":
        components.html("<script>window.parent.document.activeElement.blur();</script>", height=0)

    curr_idx = date_list.index(sel_date)
    if sel_region != "지역을 입력하세요.":
        m_val = df_maemae.loc[df_maemae['날짜'] == sel_date, sel_region].values[0]
        j_val = df_jeonse.loc[df_jeonse['날짜'] == sel_date, sel_region].values[0]
        m_color = "#e74c3c" if m_val > 0 else "#000080" if m_val < 0 else "#333"
        j_color = "#e74c3c" if j_val > 0 else "#000080" if j_val < 0 else "#333"
        
        st.markdown(f'''
            <div class="content-card">
                <div class="summary-label">📍 {sel_region} 매매 증감</div>
                <div class="summary-date">기준: {sel_date}</div>
                <div style="color:{m_color}; font-size:32px; font-weight:900;">{m_val:+.2f}%</div>
            </div>
            <div class="content-card">
                <div class="summary-label">📍 {sel_region} 전세 증감</div>
                <div class="summary-date">기준: {sel_date}</div>
                <div style="color:{j_color}; font-size:32px; font-weight:900;">{j_val:+.2f}%</div>
            </div>
        ''', unsafe_allow_html=True)

        start_idx = max(0, curr_idx - 3)
        def draw_chart(df, line_color, title):
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="chart-title">{title}</div>', unsafe_allow_html=True)
            sub_df = df.iloc[start_idx : curr_idx + 1]
            fig = px.line(sub_df, x='날짜', y=sel_region, markers=True)
            fig.update_traces(line_color=line_color, line_width=4, marker=dict(size=10, color='white', line=dict(width=2, color=line_color)))
            fig.add_scatter(x=[sel_date], y=[sub_df.loc[sub_df['날짜']==sel_date, sel_region].values[0]], 
                            mode='markers', marker=dict(size=14, color='#00FF00', line=dict(width=3, color='white')), showlegend=False)
            fig.update_layout(
                height=240, margin=dict(l=10,r=10,t=10,b=10), 
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                xaxis=dict(fixedrange=True, tickfont=dict(color='#006400', weight='bold')), 
                yaxis=dict(fixedrange=True, tickfont=dict(color='#006400', weight='bold')), 
                hovermode=False
            )
            st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})
            st.markdown('</div>', unsafe_allow_html=True)

        draw_chart(df_maemae, '#e74c3c', f'📈 {sel_region} 매매 트렌드')
        draw_chart(df_jeonse, '#000080', f'📉 {sel_region} 전세 트렌드')
        
        st.markdown("<br>", unsafe_allow_html=True)

    # 랭킹 섹션
    st.markdown('<div class="ranking-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title" style="color:#FF69B4;">🔥 주간 매매 상승 TOP 10</div>', unsafe_allow_html=True)
    m_w_row = df_maemae[df_maemae['날짜'] == sel_date].drop(columns=['날짜']).iloc[0]
    top_mw = m_w_row[m_w_row > 0].sort_values(ascending=False).head(10)
    for i, (name, val) in enumerate(top_mw.items()):
        st.markdown(f'<div class="rank-card rank-m"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if curr_idx >= 3:
        st.markdown('<div class="ranking-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title" style="color:#FF69B4;">📅 월간 매매 상승 TOP 10</div>', unsafe_allow_html=True)
        m_sum = df_maemae.iloc[curr_idx-3 : curr_idx+1].drop(columns=['날짜']).sum()
        top_mm = m_sum[m_sum > 0].sort_values(ascending=False).head(10)
        for i, (name, val) in enumerate(top_mm.items()):
            st.markdown(f'<div class="rank-card rank-m"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ranking-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title" style="color:#4169E1;">💧 주간 전세 상승 TOP 10</div>', unsafe_allow_html=True)
    j_w_row = df_jeonse[df_jeonse['날짜'] == sel_date].drop(columns=['날짜']).iloc[0]
    top_jw = j_w_row[j_w_row > 0].sort_values(ascending=False).head(10)
    for i, (name, val) in enumerate(top_jw.items()):
        st.markdown(f'<div class="rank-card rank-j"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if curr_idx >= 3:
        st.markdown('<div class="ranking-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title" style="color:#4169E1;">📅 월간 전세 상승 TOP 10</div>', unsafe_allow_html=True)
        j_sum = df_jeonse.iloc[curr_idx-3 : curr_idx+1].drop(columns=['날짜']).sum()
        top_jm = j_sum[j_sum > 0].sort_values(ascending=False).head(10)
        for i, (name, val) in enumerate(top_jm.items()):
            st.markdown(f'<div class="rank-card rank-j"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚪 앱 종료"):
        st.session_state.is_exit = True
        st.rerun()

if __name__ == "__main__":
    main()
