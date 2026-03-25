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
    
    /* 핵심 수정 1: 전체 배경에 이미지 적용 */
    .stApp {
        background-image: url("https://raw.githubusercontent.com/YourGitHubID/YourRepo/main/background.png"); /* 실제 Raw 이미지 주소로 변경 필요 */
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

    /* 입력 필드 카드화 - 그림자 효과 강화 */
    div[data-testid="stVerticalBlock"] > div:has(div[data-baseweb="select"]) {
        background: rgba(255, 255, 255, 0.85); /* 배경이 살짝 비치도록 투명도 유지 */
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); /* 수정 사항: 그림자 효과 강화 */
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    /* 입력 필드 글자 설정 */
    div[data-baseweb="select"] * {
        font-weight: 900 !important;
        font-size: 16px !important;
    }
    
    /* 커서 숨기기 */
    div[data-baseweb="select"] input {
        caret-color: transparent !important;
    }

    label[data-testid="stWidgetLabel"] p {
        font-weight: 900 !important;
        font-size: 17px !important;
        color: #333;
    }

    /* 증감/그래프 카드 스타일 - 그림자 효과 강화 */
    .content-card {
        background: rgba(255, 255, 255, 0.85); /* 배경이 살짝 비치도록 투명도 유지 */
        border-radius: 18px; 
        padding: 25px; 
        text-align: center; 
        margin-bottom: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1); /* 수정 사항: 그림자 효과 강화 */
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .summary-label { color: #555; font-size: 14px; font-weight: 700; margin-bottom: 5px; }
    
    /* 유지 사항: 기준 날짜 컬러 (진한 퍼플) */
    .summary-date { color: #800080; font-size: 11px; margin-bottom: 10px; font-weight: 700; }

    /* 랭킹 섹션 카드화 - 그림자 효과 강화 */
    .ranking-container {
        background: rgba(255, 255, 255, 0.85); /* 배경이 살짝 비치도록 투명도 유지 */
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); /* 수정 사항: 그림자 효과 강화 */
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

    /* 유지 사항: 그래프 제목 컬러 (진한 그린) */
    .chart-title {
        font-size: 19px; font-weight: 800; margin: 10px 0 15px 0;
        padding-left: 5px;
        color: #006400;
    }

    /* 버튼 스타일 */
    div.stButton {
        text-align: center;
        margin: 40px 0;
        display: flex;
        justify-content: center;
    }
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

    /* 종료 화면 - 배경 흐리게 처리 */
    .exit-wrapper {
        position: fixed; top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        width: 100%; text-align: center; z-index: 9999;
        background: rgba(255, 255, 255, 0.9);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.1);
    }
    .exit-msg { color: #006400; font-weight: 900; font-size: 32px; margin-top: 20px; }
    .exit-credit { color: #888; font-size: 18px; margin-top: 10px; }

    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ... (show_title, load_data 함수는 변경 없음)

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

    # ... (데이터 로드 및 selectbox 로직은 변경 없음)

        start_idx = max(0, curr_idx - 3)
        def draw_chart(df, line_color, title):
            # 차트를 담는 카드 시작 (CSS에 의해 그림자 효과 적용)
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="chart-title">{title}</div>', unsafe_allow_html=True)
            sub_df = df.iloc[start_idx : curr_idx + 1]
            fig = px.line(sub_df, x='날짜', y=sel_region, markers=True)
            fig.update_traces(line_color=line_color, line_width=4, marker=dict(size=10, color='white', line=dict(width=2, color=line_color)))
            fig.add_scatter(x=[sel_date], y=[sub_df.loc[sub_df['날짜']==sel_date, sel_region].values[0]], 
                            mode='markers', marker=dict(size=14, color='#00FF00', line=dict(width=3, color='white')), showlegend=False)
            
            # 유지 사항: 그래프 내부 텍스트 및 축 눈금 컬러 (진한 그린)
            fig.update_layout(
                height=240, margin=dict(l=10,r=10,t=10,b=10), 
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                xaxis=dict(fixedrange=True, tickfont=dict(color='#006400', weight='bold')), 
                yaxis=dict(fixedrange=True, tickfont=dict(color='#006400', weight='bold')), 
                hovermode=False
            )
            st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})
            st.markdown('</div>', unsafe_allow_html=True) # 카드 끝

        draw_chart(df_maemae, '#e74c3c', f'📈 {sel_region} 매매 트렌드')
        draw_chart(df_jeonse, '#000080', f'📉 {sel_region} 전세 트렌드')
        
        # ... (이하 로직 변경 없음)
