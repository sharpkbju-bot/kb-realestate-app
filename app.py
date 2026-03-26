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

# 배경 이미지를 Base64로 변환하여 주입하는 함수
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

# 배경화면 적용 (파일명: bg.jpg)
set_bg_from_local('bg.jpg')

# 2. UI 디자인 및 스타일 설정 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Noto+Sans+KR:wght@300;500;700;900&display=swap');
    
    html, body, [class*="css"] { font-family: 'Noto+Sans+KR', sans-serif; }

    /* 타이틀 스타일 */
    .title-container { width: 100%; padding: 30px 0 15px 0; text-align: center; }
    .brand-name { color: #006400; font-size: clamp(30px, 10vw, 45px); font-weight: 900; font-family: 'Arial Black'; letter-spacing: -2px; }
    .brand-suffix { color: #FF4500; font-size: clamp(16px, 5vw, 24px); font-weight: 900; }

    /* 입력 필드 글자 900 Bold 강제 적용 */
    div[data-baseweb="select"] * { font-weight: 900 !important; font-size: 16px !important; }
    
    /* 입력 필드 라벨 컬러 진한 그린 및 900 Bold */
    label[data-testid="stWidgetLabel"] p { 
        font-weight: 900 !important; 
        font-size: 17px !important; 
        color: #006400 !important; 
    }

    /* 요약 카드 */
    .summary-card { 
        background: rgba(255, 255, 255, 0.92) !important;
        border-radius: 18px; padding: 20px; text-align: center; margin-bottom: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); border: 1px solid #f0f0f0;
    }
    .summary-label { font-weight: 900; color: #000080 !important; }

    /* 랭킹 카드 공통 스타일 */
    .rank-card {
        padding: 12px 15px; border-radius: 12px; margin-bottom: 12px;
        display: flex; align-items: center; justify-content: space-between;
        background: linear-gradient(135deg, rgba(243, 229, 245, 0.95), rgba(225, 190, 231, 0.95)) !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5) !important, inset 0 2px 5px rgba(255,255,255,0.5) !important; 
        border: 1px solid rgba(103, 58, 183, 0.2);
    }
    .rank-info { display: flex; align-items: center; gap: 8px; }
    .rank-num { font-weight: 900; font-size: 16px; color: #4a148c !important; }
    .rank-name { font-weight: 900; font-size: 16px; }
    .rank-val { font-weight: 900; font-size: 15px; }
    
    /* 매매 상승 TOP 10 카드 내 지역명 및 상승률 브라운(#8B4513) */
    .rank-m { border-left: 7px solid #FF4500; }
    .rank-m .rank-name, .rank-m .rank-val { color: #8B4513 !important; }

    /* 전세 상승 TOP 10 카드 내 지역명 및 상승률 청녹색(#008080) */
    .rank-j { border-left: 7px solid #000080; }
    .rank-j .rank-name, .rank-j .rank-val { color: #008080 !important; }

    /* 트렌드 차트 제목 컬러 진한 그린(#006400) */
    .chart-title { font-size: 19px; font-weight: 900; margin: 30px 0 15px 0; padding-left: 12px; color: #006400; }

    /* 공통 버튼 스타일 */
    div.stButton { display: flex; justify-content: center; margin: 20px 0; }
    div.stButton > button {
        /* [수정 사항] 글자색 하늘색으로 수정 */
        color: #87CEEB !important; /* 하늘색 */
        border-radius: 25px !important;
        width: 100% !important; max-width: 400px !important; height: 60px !important; font-weight: 900 !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3) !important; border: none !important;
        font-size: 20px !important;
    }

    /* [수정 사항] 스크린샷 버튼 전용 스타일 수정 (배경 연한 그린, 글자 하늘색) */
    div.stButton.screenshot-btn > button {
        background: #90EE90 !important; /* 연한 그린 (LightGreen) */
    }

    /* [수정 사항] 종료 버튼 전용 스타일 수정 (배경 연한 퍼플, 글자 하늘색) */
    div.stButton.exit-btn > button {
        background: #E6E6FA !important; /* 연한 퍼플 (Lavender) */
    }

    /* 종료 화면 스타일 */
    .exit-wrapper {
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
        width: 100%; text-align: center; z-index: 9999;
    }
    .exit-msg { color: #006400; font-weight: 900; font-size: 32px; margin-top: 20px; }
    
    /* Created by 필기체 스타일 (네이비) */
    .created-by { 
        font-family: 'Dancing Script', 'Brush Script MT', cursive !important;
        color: #000080 !important;
        font-size: 30px !important; 
        font-weight: 700 !important;
        margin-top: 10px;
    }

    /* 자산가 문구 스타일 (진한 노란색) */
    .asset-info {
        font-weight: 900;
        color: #FFD700 !important; 
        font-size: 20px !important;
        margin-top: 5px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }

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
                <div class="title-container">
                    <span class="brand-name">Dr.J</span><span class="brand-suffix">의 부동산</span>
                </div>
                <div class="exit-msg">모두 부자됩시다.</div>
                <div class="created-by">Created by Ju Kyung Bae</div>
                <div class="asset-info">with 70억 자산가 이승연</div>
            </div>
        """, unsafe_allow_html=True)
        components.html("<script>window.close();</script>")
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
            
            # 그래프 내부의 x축(날짜)과 y축(지역명) 라벨 컬러 시안과 동일한 네이비 컬러(#000080)
            fig.update_layout(
                height=220, 
                margin=dict(l=10,r=10,t=10,b=10), 
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)', 
                hovermode=False, 
                dragmode=False, 
                font=dict(color='#000080', size=12),
                xaxis=dict(
                    fixedrange=True, 
                    tickfont=dict(color='#000080', weight='bold'),
                    title=dict(font=dict(color='#000080'))
                ),
                yaxis=dict(
                    fixedrange=True, 
                    tickfont=dict(color='#000080', weight='bold'),
                    title=dict(text="", font=dict(color='#000080'))
                )
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'scrollZoom': False})

        draw_chart(df_maemae, '#e74c3c', f'📈 {sel_region} 매매 트렌드 (4주)')
        draw_chart(df_jeonse, '#000080', f'📉 {sel_region} 전세 트렌드 (4주)')
        st.markdown("<hr>", unsafe_allow_html=True)

    # --- 랭킹 섹션 (풀 버전) ---
    # 1. 주간 매매 TOP 10
    st.markdown('<div class="chart-title" style="color:#FF4500; border-left:6px solid #FF4500;">🔥 주간 매매 상승 TOP 10</div>', unsafe_allow_html=True)
    m_w_row = df_maemae[df_maemae['날짜'] == sel_date].drop(columns=['날짜']).iloc[0]
    top_mw = m_w_row[m_w_row > 0].sort_values(ascending=False).head(10)
    for i, (name, val) in enumerate(top_mw.items()):
        st.markdown(f'<div class="rank-card rank-m"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    # 2. 월간 매매 TOP 10
    if curr_idx >= 3:
        st.markdown('<div class="chart-title" style="color:#FF4500; border-left:6px solid #FF4500;">📅 월간 매매 상승 TOP 10</div>', unsafe_allow_html=True)
        m_m_sum = df_maemae.iloc[curr_idx-3 : curr_idx+1].drop(columns=['날짜']).sum()
        top_mm = m_m_sum[m_m_sum > 0].sort_values(ascending=False).head(10)
        for i, (name, val) in enumerate(top_mm.items()):
            st.markdown(f'<div class="rank-card rank-m"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    # 3. 주간 전세 TOP 10
    st.markdown('<div class="chart-title" style="color:#FF1493; border-left:6px solid #FF1493;">💧 주간 전세 상승 TOP 10</div>', unsafe_allow_html=True)
    j_w_row = df_jeonse[df_jeonse['날짜'] == sel_date].drop(columns=['날짜']).iloc[0]
    top_jw = j_w_row[j_w_row > 0].sort_values(ascending=False).head(10)
    for i, (name, val) in enumerate(top_jw.items()):
        st.markdown(f'<div class="rank-card rank-j"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    # 4. 월간 전세 TOP 10
    if curr_idx >= 3:
        st.markdown('<div class="chart-title" style="color:#FF1493; border-left:6px solid #FF1493;">📅 월간 전세 상승 TOP 10</div>', unsafe_allow_html=True)
        j_m_sum = df_jeonse.iloc[curr_idx-3 : curr_idx+1].drop(columns=['날짜']).sum()
        top_jm = j_m_sum[j_m_sum > 0].sort_values(ascending=False).head(10)
        for i, (name, val) in enumerate(top_jm.items()):
            st.markdown(f'<div class="rank-card rank-j"><div class="rank-info"><span class="rank-num">{i+1}위</span> <span class="rank-name">{name}</span></div><span class="rank-val">+{val:.2f}%</span></div>', unsafe_allow_html=True)

    # --- 하단 버튼 섹션 ---
    # [수정 사항] 스크린샷 버튼 (JS 주입을 위한 ID 부여 및 key 설정)
    st.markdown('<div class="stButton screenshot-btn">', unsafe_allow_html=True)
    screenshot_clicked = st.button("📸 화면 스크린샷", key="screenshot_trigger")
    st.markdown('</div>', unsafe_allow_html=True)

    # [수정 사항] 종료 버튼 (JS 주입을 위한 ID 부여 및 key 설정)
    st.markdown('<div class="stButton exit-btn">', unsafe_allow_html=True)
    if st.button("🚪 앱 종료", key="exit_trigger"):
        st.session_state.is_exit = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # [수정 사항] 스크린샷 캡처 및 공유를 위한 JavaScript 로직 (Dancing Script 등 폰트 렌더링 포함)
    st.markdown(
        """
        <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
        <script>
        const screenshotBtn = parent.document.querySelector('button[key="screenshot_trigger"]');
        
        if (screenshotBtn) {
            screenshotBtn.addEventListener('click', function() {
                const captureTarget = parent.document.querySelector('#root');
                
                html2canvas(captureTarget, {
                    useCORS: true,
                    logging: false,
                    backgroundColor: null
                }).then(canvas => {
                    const dataUrl = canvas.toDataURL('image/png');
                    
                    if (navigator.share) {
                        fetch(dataUrl)
                            .then(res => res.blob())
                            .then(blob => {
                                const file = new File([blob], 'DrJ_RealEstate_Screen.png', { type: 'image/png' });
                                navigator.share({
                                    files: [file],
                                    title: 'Dr.J의 부동산 화면 공유',
                                    text: '오늘의 부동산 트렌드를 공유합니다!'
                                }).catch(err => console.error('Share failed:', err));
                            });
                    } else {
                        const link = document.createElement('a');
                        link.href = dataUrl;
                        link.download = 'DrJ_RealEstate_Screen.png';
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                        alert('스크린샷이 다운로드 폴더에 저장되었습니다.');
                    }
                });
            });
        }
        </script>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
