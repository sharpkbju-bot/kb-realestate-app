import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import base64
import os

# 1. 페이지 설정
st.set_page_config(page_title="Dr.J의 부동산", page_icon="🏠", layout="centered")

# 세션 상태 초기화
if "clicked_region" not in st.session_state:
    st.session_state.clicked_region = "지역을 입력하세요."

# 배경 이미지 처리
def set_bg_from_local(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded_string}");
                background-size: cover; background-attachment: fixed; background-position: center;
            }}
            </style>""", unsafe_allow_html=True)

set_bg_from_local('bg.jpg')

# 2. 스타일 설정 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto+Sans+KR', sans-serif; scroll-behavior: smooth; }

    /* 최상단 앵커 포인트 */
    #top-anchor { position: absolute; top: 0; height: 0; }

    .title-container { width: 100%; padding: 30px 0 15px 0; text-align: center; }
    .brand-name { color: #006400; font-size: clamp(30px, 10vw, 45px); font-weight: 900; font-family: 'Arial Black'; letter-spacing: -2px; }
    .brand-suffix { color: #FF4500; font-size: clamp(16px, 5vw, 24px); font-weight: 900; }

    /* 필드명(Label) 컬러를 진한 그린색으로 변경 */
    label[data-testid="stWidgetLabel"] p { 
        color: #006400 !important; /* 진한 그린색 */
        font-weight: 900 !important; 
        font-size: 18px !important; 
    }

    /* 입력 필드 내부 텍스트 스타일 */
    div[data-baseweb="select"] * { font-weight: 900 !important; font-size: 16px !important; }

    /* 요약 정보 카드 */
    .summary-card {
        background: rgba(255, 255, 255, 0.92) !important;
        border-radius: 18px; padding: 20px; text-align: center; margin-bottom: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); border: 1px solid #f0f0f0;
    }

    /* 랭킹 버튼 - 100% 확장 및 강력한 그림자 */
    div.stButton > button[key^="btn_"] {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 12px !important;
        padding: 20px 25px !important;
        width: 100% !important; 
        min-height: 70px !important;
        border: 1px solid rgba(0,0,0,0.1) !important;
        box-shadow: 0 12px 30px rgba(0,0,0,0.4) !important;
        color: #111 !important;
        font-weight: 900 !important;
        font-size: 18px !important;
        text-align: left !important;
        margin-bottom: 10px !important;
    }

    .chart-title { font-size: 20px; font-weight: 900; margin: 30px 0 15px 0; padding-left: 12px; color: #333; }

    /* 종료 버튼 */
    div.stButton > button:not([key^="btn_"]) {
        background: linear-gradient(135deg, #757575, #424242) !important;
        color: white !important; border-radius: 25px !important;
        width: 180px !important; height: 50px !important; margin: 0 auto; display: block;
    }

    header {visibility: hidden;}
    [data-testid="stPlotlyChart"] { background-color: transparent !important; }
    hr { border: 0; height: 1px; background: rgba(0,0,0,0.1); margin: 35px 0; }
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
    
    for df in [df_m, df_j]:
        for col in df.columns:
            if col != '날짜':
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    common_cols = ['날짜'] + sorted(list(set(df_m.columns) & set(df_j.columns) - {'날짜'}))
    return df_m[common_cols], df_j[common_cols]

def main():
    st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

    if st.session_state.get("is_exit"):
        st.markdown("""<div style='text-align:center; margin-top:40vh;'><h1 style='color:#006400; font-weight:900;'>모두 부자됩시다.</h1></div>""", unsafe_allow_html=True)
        components.html("<script>window.close();</script>")
        st.stop()

    st.markdown('<div class="title-container"><span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span></div>', unsafe_allow_html=True)

    df_maemae, df_jeonse = load_data()
    date_list = sorted(df_maemae['날짜'].unique().tolist())
    region_list = sorted([col for col in df_maemae.columns if col != '날짜'])

    sel_date = st.selectbox("📅 날짜 선택", date_list, index=len(date_list)-1)
    
    if st.session_state.clicked_region in region_list:
        default_idx = region_list.index(st.session_state.clicked_region) + 1
    else:
        default_idx = 0

    sel_region = st.selectbox("🔍 지역 검색 및 선택", options=["지역을 입력하세요."] + region_list, index=default_idx)

    if sel_region != "지역을 입력하세요.":
        st.session_state.clicked_region = sel_region
        curr_idx = date_list.index(sel_date)
        
        m_val = df_maemae.loc[df_maemae['날짜'] == sel_date, sel_region].values[0]
        j_val = df_jeonse.loc[df_jeonse['날짜'] == sel_date, sel_region].values[0]
        m_color = "#e74c3c" if m_val > 0 else "#000080" if m_val < 0 else "#333"
        j_color = "#e74c3c" if j_val > 0 else "#000080" if j_val < 0 else "#333"
        
        st.markdown(f'''
            <div class="summary-card">
                <div style="color:#666; font-size:14px; font-weight:700;">📍 {sel_region} 매매 증감 ({sel_date})</div>
                <div style="color:{m_color}; font-size:32px; font-weight:900;">{m_val:+.2f}%</div>
            </div>
            <div class="summary-card">
                <div style="color:#666; font-size:14px; font-weight:700;">📍 {sel_region} 전세 증감 ({sel_date})</div>
                <div style="color:{j_color}; font-size:32px; font-weight:900;">{j_val:+.2f}%</div>
            </div>''', unsafe_allow_html=True)

        start_idx = max(0, curr_idx - 3)
        def draw_chart(df, color, title):
            st.markdown(f'<div class="chart-title">{title}</div>', unsafe_allow_html=True)
            sub_df = df.iloc[start_idx : curr_idx + 1]
            fig = px.line(sub_df, x='날짜', y=sel_region, markers=True)
            fig.update_traces(line_color=color, line_width=4, marker=dict(size=12, color='white', line=dict(width=3, color=color)))
            fig.update_layout(height=240, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', hovermode=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        draw_chart(df_maemae, '#e74c3c', f'📈 {sel_region} 매매 트렌드')
        draw_chart(df_jeonse, '#000080', f'📉 {sel_region} 전세 트렌드')
        st.markdown("<hr>", unsafe_allow_html=True)

    def render_rank(df, date_idx, title, color, is_monthly=False):
        st.markdown(f'<div class="chart-title" style="color:{color}; border-left:6px solid {color};">{title}</div>', unsafe_allow_html=True)
        numeric_df = df.drop(columns=['날짜'])
        data = numeric_df.iloc[max(0, date_idx-3) : date_idx+1].sum() if is_monthly else numeric_df.iloc[date_idx]
        top_10 = data[data > 0].sort_values(ascending=False).head(10)
        for i, (name, val) in enumerate(top_10.items()):
            label = f"{i+1}위  |  {name}  |  +{val:.2f}%"
            if st.button(label, key=f"btn_{title}_{name}"):
                st.session_state.clicked_region = name
                components.html("<script>window.parent.document.querySelector('section.main').scrollTo({top: 0, behavior: 'smooth'});</script>", height=0)
                st.rerun()

    curr_idx = date_list.index(sel_date)
    render_rank(df_maemae, curr_idx, "🔥 주간 매매 상승 TOP 10", "#FF4500")
    if curr_idx >= 3: render_rank(df_maemae, curr_idx, "📅 월간 매매 상승 TOP 10", "#FF4500", True)
    render_rank(df_jeonse, curr_idx, "💧 주간 전세 상승 TOP 10", "#000080")
    if curr_idx >= 3: render_rank(df_jeonse, curr_idx, "📅 월간 전세 상승 TOP 10", "#000080", True)

    st.markdown('<div style="margin-top:50px; margin-bottom:100px;">', unsafe_allow_html=True)
    if st.button("🚪 앱 종료", key="exit_btn"):
        st.session_state.is_exit = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
