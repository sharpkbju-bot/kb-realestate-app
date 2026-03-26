import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import base64
import os

# 1. 페이지 설정
st.set_page_config(
    page_title="Dr.J의 부동산", 
    page_icon="🏠",
    layout="centered"
)

# 배경 이미지 주입 함수
def set_bg_from_local(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded_string}");
                background-size: cover;
                background-attachment: fixed;
                background-position: center;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

set_bg_from_local('bg.jpg')

# 2. UI 디자인 및 스타일 설정 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    
    html, body, [class*="css"] { font-family: 'Noto+Sans+KR', sans-serif; }

    .title-container { width: 100%; padding: 30px 0 15px 0; text-align: center; }
    .brand-name { color: #006400; font-size: clamp(30px, 10vw, 45px); font-weight: 900; font-family: 'Arial Black'; letter-spacing: -2px; }
    .brand-suffix { color: #FF4500; font-size: clamp(16px, 5vw, 24px); font-weight: 900; }

    div[data-baseweb="select"] * { font-weight: 900 !important; font-size: 16px !important; }
    label[data-testid="stWidgetLabel"] p { font-weight: 900 !important; font-size: 17px !important; color: #006400 !important; }

    .summary-card { 
        background: rgba(255, 255, 255, 0.92) !important;
        border-radius: 18px; padding: 20px; text-align: center; margin-bottom: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); border: 1px solid #f0f0f0;
    }
    .summary-label { font-weight: 900; color: #000080 !important; }

    .rank-card {
        padding: 12px 15px; border-radius: 12px; margin-bottom: 12px;
        display: flex; align-items: center; justify-content: space-between;
        background: linear-gradient(135deg, rgba(243, 229, 245, 0.95), rgba(225, 190, 231, 0.95)) !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5) !important, inset 0 2px 5px rgba(255,255,255,0.5) !important; 
        border: 1px solid rgba(103, 58, 183, 0.2);
    }
    .rank-num { font-weight: 900; font-size: 16px; color: #4a148c !important; }
    .rank-name, .rank-val { font-weight: 900; font-size: 16px; }
    
    .rank-m { border-left: 7px solid #FF4500; }
    .rank-m .rank-name, .rank-m .rank-val { color: #8B4513 !important; }
    .rank-j { border-left: 7px solid #000080; }
    .rank-j .rank-name, .rank-j .rank-val { color: #008080 !important; }

    .chart-title { font-size: 19px; font-weight: 900; margin: 30px 0 15px 0; padding-left: 12px; color: #006400; }

    /* [수정] 하단 커스텀 버튼 스타일 (높이를 55px -> 48px로 슬림하게 조정) */
    .custom-btn-group { display: flex; flex-direction: column; width: 100%; margin-top: 20px; }
    .custom-btn {
        width: 100%; 
        height: 48px; /* 슬림하게 변경 */
        border-radius: 12px; font-weight: 900; font-size: 17px; /* 폰트 사이즈 살짝 조정 */
        color: #87CEEB !important; display: flex; justify-content: center; align-items: center;
        text-decoration: none !important; border: 2px solid rgba(200, 200, 200, 0.6);
        background: linear-gradient(135deg, rgba(60, 60, 60, 0.8), rgba(30, 30, 30, 0.9));
        box-shadow: 0 5px 15px rgba(0,0,0,0.3); cursor: pointer; transition: all 0.3s ease;
    }
    .custom-btn:hover {
        border-color: rgba(255, 255, 255, 0.8);
        background: linear-gradient(135deg, rgba(80, 80, 80, 0.9), rgba(50, 50, 50, 1));
    }
    .exit-btn-margin { margin-top: 11px !important; } /* 3mm 간격 유지 */

    .exit-wrapper { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 100%; text-align: center; z-index: 9999; }
    .exit-msg { color: #006400; font-weight: 900; font-size: 32px; margin-top: 20px; }
    .created-by { font-family: 'Dancing Script', cursive !important; color: #000080 !important; font-size: 30px !important; font-weight: 700 !important; margin-top: 10px; }
    .asset-info { font-weight: 900; color: #FFD700 !important; font-size: 20px !important; margin-top: 5px; text-shadow: 1px 1px 2px rgba(0,0,0,0.2); }

    [data-testid="stPlotlyChart"] { background-color: transparent !important; }
    header {visibility: hidden;}
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
                <div class="title-container"><span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span></div>
                <div class="exit-msg">모두 부자됩시다.</div>
                <div class="created-by">Created by Ju Kyung Bae</div>
                <div class="asset-info">with 70억 자산가 이승연</div>
            </div>
        """, unsafe_allow_html=True)
        st.stop()

    st.markdown('<div class="title-container"><span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span></div>', unsafe_allow_html=True)

    df_maemae, df_jeonse = load_data()
    date_list = sorted(df_maemae['날짜'].unique().tolist())
    region_list = sorted([col for col in df_maemae.columns if col != '날짜'])

    sel_date = st.selectbox("📅 날짜 선택", date_list, index=len(date_list)-1)
    sel_region = st.selectbox("🔍 지역 검색 및 선택", options=["지역을 입력하세요."] + region_list, index=0)

    curr_idx = date_list.index(sel_date)

    if sel_region != "지역을 입력하세요.":
        components.html("<script>window.parent.document.activeElement.blur();</script>", height=0)
        m_val = df_maemae.loc[df_maemae['날짜'] == sel_date, sel_region].values[0]
        j_val = df_jeonse.loc[df_jeonse['날짜'] == sel_date, sel_region].values[0]
        
        m_color = "#e74c3c" if m_val > 0 else "#000080" if m_val < 0 else "#333"
        j_color = "#e74c3c" if j_val > 0 else "#000080" if j_val < 0 else "#333"
        
        st.markdown(f'''
            <div class="summary-card">
                <div class="summary-label">📍 {sel_region} 매매 증감 ({sel_date})</div>
                <div style="color:{m_color}; font-size:28px; font-weight:900;">{m_val:+.2f}%</div>
            </div>
            <div class="summary-card">
                <div class="summary-label">📍 {sel_region} 전세 증감 ({sel_date})</div>
                <div style="color:{j_color}; font-size:28px; font-weight:900;">{j_val:+.2f}%</div>
            </div>
        ''', unsafe_allow_html=True)

        start_idx = max(0, curr_idx - 3)
        def draw_chart(df, line_color, title):
            st.markdown(f'<div class="chart-title">{title}</div>', unsafe_allow_html=True)
            sub_df = df.iloc[start_idx : curr_idx + 1]
            fig = px.line(sub_df, x='날짜', y=sel_region, markers=True)
            fig.update_traces(line_color=line_color, line_width=4, marker=dict(size=10, color='white', line=dict(width=2, color=line_color)))
            fig.update_layout(
                height=220, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                font=dict(color='#000080', size=12),
                xaxis=dict(fixedrange=True, tickfont=dict(color='#000080', weight='bold'), title=dict(font=dict(color='#000080'))),
                yaxis=dict(fixedrange=True, tickfont=dict(color='#000080', weight='bold'), title=dict(text="", font=dict(color='#000080')))
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        draw_chart(df_maemae, '#e74c3c', f'📈 {sel_region} 매매 트렌드 (4주)')
        draw_chart(df_jeonse, '#000080', f'📉 {sel_region} 전세 트렌드 (4주)')
        st.markdown("<hr>", unsafe_allow_html=True)

    # 랭킹 섹션 복원
    st.markdown('<div class="chart-title" style="color:#FF4500; border-left:6px solid #FF4500;">🔥 주간 매매 상승 TOP 10</div>', unsafe_allow_html=True)
    m_w_row = df_maemae[df_maemae['날짜'] == sel_date].drop(columns=['날짜']).iloc[0]
    top_mw = m_w_row[m_w_row > 0].sort_values(ascending=False).head(10)
    for i, (name, val) in enumerate(top_mw.items()):
        st.markdown(f'<div class="rank-card rank-m"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    if curr_idx >= 3:
        st.markdown('<div class="chart-title" style="color:#FF4500; border-left:6px solid #FF4500;">📅 월간 매매 상승 TOP 10</div>', unsafe_allow_html=True)
        m_m_sum = df_maemae.iloc[curr_idx-3 : curr_idx+1].drop(columns=['날짜']).sum()
        top_mm = m_m_sum[m_m_sum > 0].sort_values(ascending=False).head(10)
        for i, (name, val) in enumerate(top_mm.items()):
            st.markdown(f'<div class="rank-card rank-m"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-title" style="color:#FF1493; border-left:6px solid #FF1493;">💧 주간 전세 상승 TOP 10</div>', unsafe_allow_html=True)
    j_w_row = df_jeonse[df_jeonse['날짜'] == sel_date].drop(columns=['날짜']).iloc[0]
    top_jw = j_w_row[j_w_row > 0].sort_values(ascending=False).head(10)
    for i, (name, val) in enumerate(top_jw.items()):
        st.markdown(f'<div class="rank-card rank-j"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    if curr_idx >= 3:
        st.markdown('<div class="chart-title" style="color:#FF1493; border-left:6px solid #FF1493;">📅 월간 전세 상승 TOP 10</div>', unsafe_allow_html=True)
        j_m_sum = df_jeonse.iloc[curr_idx-3 : curr_idx+1].drop(columns=['날짜']).sum()
        top_jm = j_m_sum[j_m_sum > 0].sort_values(ascending=False).head(10)
        for i, (name, val) in enumerate(top_jm.items()):
            st.markdown(f'<div class="rank-card rank-j"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    # [수정] 슬림해진 하단 커스텀 버튼 섹션
    st.markdown("""
        <div class="custom-btn-group">
            <div id="btn-screenshot" class="custom-btn">📸 화면 스크린샷</div>
            <div id="btn-exit" class="custom-btn exit-btn-margin">🚪 앱 종료</div>
        </div>
    """, unsafe_allow_html=True)

    if st.query_params.get("action") == "exit":
        st.session_state.is_exit = True
        st.query_params.clear()
        st.rerun()

    st.markdown(
        """
        <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
        <script>
        const scBtn = window.parent.document.getElementById('btn-screenshot');
        if (scBtn) {
            scBtn.onclick = function() {
                const target = window.parent.document.querySelector('#root');
                html2canvas(target, { useCORS: true, logging: false }).then(canvas => {
                    const dataUrl = canvas.toDataURL('image/png');
                    const link = document.createElement('a'); link.href = dataUrl; link.download = 'DrJ_RealEstate.png';
                    link.click();
                });
            };
        }
        const exBtn = window.parent.document.getElementById('btn-exit');
        if (exBtn) {
            exBtn.onclick = function() {
                const url = new URL(window.parent.location);
                url.searchParams.set('action', 'exit');
                window.parent.location.href = url.href;
            };
        }
        </script>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
