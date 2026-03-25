import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정: 이 설정이 PWA 설치 시 앱의 이름과 아이콘을 결정합니다.
st.set_page_config(
    page_title="Dr.J의 부동산", 
    page_icon="🏠",
    layout="centered"
)

# 2. 디자인 및 레이아웃 수정 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Noto+Sans+KR', sans-serif;
    }

    /* 타이틀 영역: Dr.J 강조 및 한 줄 정렬 */
    .title-container {
        padding: 40px 0 20px 0;
        text-align: center;
        width: 100%;
    }
    
    .main-title {
        display: flex;
        align-items: baseline;
        justify-content: center;
        gap: 8px;
        white-space: nowrap;
    }
    
    .brand-name {
        color: #006400; /* 짙은 그린 */
        font-size: clamp(32px, 10vw, 48px); /* Dr.J를 매우 크게 설정 */
        font-weight: 900;
        font-family: 'Arial Black', sans-serif;
        line-height: 1;
    }
    
    .brand-suffix {
        color: #333;
        font-size: clamp(18px, 5vw, 26px); /* '의 부동산'은 상대적으로 작게 */
        font-weight: 700;
    }

    /* 지역명 강조 (짙은 핑크) */
    .selected-region-text {
        color: #DB7093;
        font-weight: 700;
    }

    /* 수치 카드 디자인 */
    .metric-container {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        text-align: center;
    }
    
    .metric-label { font-size: 14px; color: #888; margin-bottom: 5px; }
    .metric-value { font-size: 28px; font-weight: 700; }

    /* 불필요한 기본 요소 숨기기 */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding-top: 1rem !important;
    }

    /* 그래프 섹션 타이틀 */
    .chart-title {
        font-size: 16px;
        font-weight: 700;
        margin: 30px 0 10px 0;
        color: #444;
        border-left: 5px solid #006400;
        padding-left: 12px;
    }
    </style>
    
    <div class="title-container">
        <div class="main-title">
            <span class="brand-name">Dr.J</span>
            <span class="brand-suffix">의 부동산</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # 파일명은 깃허브 저장소와 일치해야 함
    try:
        df_m = pd.read_csv('maemae.csv', encoding='cp949')
        df_j = pd.read_csv('jeonse.csv', encoding='cp949')
    except:
        df_m = pd.read_csv('maemae.csv', encoding='utf-8')
        df_j = pd.read_csv('jeonse.csv', encoding='utf-8')
    
    df_m['날짜'] = df_m['날짜'].astype(str)
    df_j['날짜'] = df_j['날짜'].astype(str)
    return df_m, df_j

def create_chart(df, region, date, color):
    # 날짜 기준 최근 4주 데이터 필터링
    df_sorted = df.sort_values(by='날짜')
    idx_list = df_sorted.index[df_sorted['날짜'] == date].tolist()
    if not idx_list: return None
    
    idx = idx_list[0]
    start_idx = max(0, idx - 3)
    recent_df = df_sorted.iloc[start_idx : idx + 1]
    
    fig = px.line(recent_df, x='날짜', y=region, markers=True)
    fig.update_traces(line_color=color, line_width=4, marker=dict(size=10, borderwidth=2, bordercolor="white"))
    fig.update_layout(
        height=220,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, title="", tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title="", tickfont=dict(size=10)),
        hovermode="x unified"
    )
    return fig

def main():
    try:
        df_maemae, df_jeonse = load_data()
        
        # 상단 입력 영역
        col_date, col_search = st.columns([1, 1.5])
        with col_date:
            date_list = df_maemae['날짜'].unique().tolist()
            selected_date = st.selectbox("📅 날짜 선택", date_list, index=len(date_list)-1)

        region_list = [col for col in df_maemae.columns if col != '날짜']
        with col_search:
            selected_region = st.selectbox("🔍 지역 검색 및 선택", options=["지역을 입력하세요"] + region_list)

        st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)

        if selected_region != "지역을 입력하세요.":
            m_val = df_maemae.loc[df_maemae['날짜'] == selected_date, selected_region].values[0]
            j_val = df_jeonse.loc[df_jeonse['날짜'] == selected_date, selected_region].values[0]

            st.markdown(f"#### 📍 <span class='selected-region-text'>{selected_region}</span> 시황", unsafe_allow_html=True)
            
            # 수치 카드 레이아웃
            c1, c2 = st.columns(2)
            # 상승(빨강), 하락(네이비 #000080), 보합(#333)
            m_color = "#e74c3c" if m_val > 0 else "#000080" if m_val < 0 else "#333"
            j_color = "#e74c3c" if j_val > 0 else "#000080" if j_val < 0 else "#333"

            with c1:
                st.markdown(f'<div class="metric-container"><div class="metric-label">매매 증감</div><div class="metric-value" style="color: {m_color};">{m_val:+.2f}%</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="metric-container"><div class="metric-label">전세 증감</div><div class="metric-value" style="color: {j_color};">{j_val:+.2f}%</div></div>', unsafe_allow_html=True)

            # 트렌드 그래프
            st.markdown('<div class="chart-title">매매 지수 트렌드 (최근 4주)</div>', unsafe_allow_html=True)
            fig_m = create_chart(df_maemae, selected_region, selected_date, "#e74c3c")
            if fig_m: st.plotly_chart(fig_m, use_container_width=True, config={'displayModeBar': False})

            st.markdown('<div class="chart-title">전세 지수 트렌드 (최근 4주)</div>', unsafe_allow_html=True)
            fig_j = create_chart(df_jeonse, selected_region, selected_date, "#000080")
            if fig_j: st.plotly_chart(fig_j, use_container_width=True, config={'displayModeBar': False})

        else:
            st.info("조회할 지역명을 입력하거나 리스트에서 선택해 주세요.")

    except Exception as e:
        st.error(f"데이터 로드 중 오류가 발생했습니다. 파일명과 형식을 확인해주세요. ({e})")

if __name__ == "__main__":
    main()
