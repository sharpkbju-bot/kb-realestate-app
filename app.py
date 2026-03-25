
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(
    page_title="Dr.J의 부동산", 
    page_icon="🏠",
    layout="centered"
)

# 2. 디자인 고도화 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Noto+Sans+KR', sans-serif;
    }

    /* 타이틀 영역 */
    .title-container {
        padding: 45px 0 25px 0;
        text-align: center;
        width: 100%;
    }
    
    .main-title {
        display: flex;
        align-items: baseline;
        justify-content: center;
        gap: 10px;
        white-space: nowrap;
    }
    
    .brand-name {
        color: #006400;
        font-size: clamp(40px, 14vw, 56px);
        font-weight: 900;
        font-family: 'Arial Black', sans-serif;
        line-height: 0.8;
        letter-spacing: -3px;
    }
    
    .brand-suffix {
        color: #333;
        font-size: clamp(20px, 6vw, 30px);
        font-weight: 700;
    }

    /* 지역명 강조 */
    .selected-region-text {
        color: #DB7093;
        font-weight: 700;
        font-size: 1.2em;
    }

    /* 수치 카드 디자인 및 간격 조정 */
    .metric-container {
        background-color: white;
        padding: 22px;
        border-radius: 18px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.06);
        border: 1px solid #f0f0f0;
        text-align: center;
        margin-bottom: 15px; /* 카드 아래쪽 여백 */
    }
    
    /* 매매/전세 증감 글자: 진한 퍼플 & 굵게 */
    .metric-label { 
        font-size: 15px; 
        color: #4B0082; /* Indigo/Deep Purple */
        font-weight: 800; 
        margin-bottom: 8px; 
    }
    
    .metric-value { font-size: 30px; font-weight: 700; }

    /* 그래프 섹션 타이틀: 진한 핑크 & 굵게 */
    .chart-title {
        font-size: 18px;
        font-weight: 800;
        margin: 40px 0 15px 0;
        color: #C71585; /* Medium Violet Red (진한 핑크) */
        border-left: 6px solid #C71585;
        padding-left: 14px;
    }

    /* 카드 사이 간격 조절을 위한 Streamlit 컬럼 커스텀 */
    [data-testid="column"] {
        padding: 0 10px !important; /* 컬럼 좌우 간격 추가 */
    }

    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container { padding-top: 0.5rem !important; }
    .static-chart { pointer-events: none !important; }
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
    df_sorted = df.sort_values(by='날짜')
    idx_list = df_sorted.index[df_sorted['날짜'] == date].tolist()
    if not idx_list: return None
    
    idx = idx_list[0]
    start_idx = max(0, idx - 3)
    recent_df = df_sorted.iloc[start_idx : idx + 1]
    
    fig = px.line(recent_df, x='날짜', y=region, markers=True)
    fig.update_traces(
        line_color=color, 
        line_width=4, 
        marker=dict(size=12, line=dict(width=2, color='white')),
        hoverinfo='skip'
    )
    fig.update_layout(
        height=240,
        margin=dict(l=15, r=15, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, title="", tickfont=dict(size=11), fixedrange=True),
        yaxis=dict(showgrid=True, gridcolor='#f2f2f2', title="", tickfont=dict(size=11), fixedrange=True),
        hovermode=False,
        dragmode=False
    )
    return fig

def main():
    try:
        df_maemae, df_jeonse = load_data()
        
        col_date, col_search = st.columns([1, 1.5])
        with col_date:
            date_list = df_maemae['날짜'].unique().tolist()
            selected_date = st.selectbox("📅 날짜 선택", date_list, index=len(date_list)-1)

        region_list = [col for col in df_maemae.columns if col != '날짜']
        with col_search:
            selected_region = st.selectbox("🔍 지역 검색 및 선택", options=["지역을 입력하세요."] + region_list)

        st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)

        if selected_region != "지역을 입력하세요.":
            if selected_region in df_maemae.columns:
                m_val = df_maemae.loc[df_maemae['날짜'] == selected_date, selected_region].values[0]
                j_val = df_jeonse.loc[df_jeonse['날짜'] == selected_date, selected_region].values[0]

                st.markdown(f"#### 📍 <span class='selected-region-text'>{selected_region}</span> 시황", unsafe_allow_html=True)
                
                # 카드 사이 간격(Gap) 확보를 위해 컬럼 생성
                c1, c2 = st.columns(2)
                m_color = "#e74c3c" if m_val > 0 else "#000080" if m_val < 0 else "#333"
                j_color = "#e74c3c" if j_val > 0 else "#000080" if j_val < 0 else "#333"

                with c1:
                    st.markdown(f'<div class="metric-container"><div class="metric-label">전주 대비 매매 증감</div><div class="metric-value" style="color: {m_color};">{m_val:+.2f}%</div></div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div class="metric-container"><div class="metric-label">전주 대비 전세 증감</div><div class="metric-value" style="color: {j_color};">{j_val:+.2f}%</div></div>', unsafe_allow_html=True)

                # 매매 그래프 (진한 핑크 타이틀)
                st.markdown('<div class="chart-title">매매 지수 트렌드 (최근 4주)</div>', unsafe_allow_html=True)
                fig_m = create_chart(df_maemae, selected_region, selected_date, "#e74c3c")
                if fig_m:
                    st.markdown('<div class="static-chart">', unsafe_allow_html=True)
                    st.plotly_chart(fig_m, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
                    st.markdown('</div>', unsafe_allow_html=True)

                # 전세 그래프 (진한 핑크 타이틀)
                st.markdown('<div class="chart-title">전세 지수 트렌드 (최근 4주)</div>', unsafe_allow_html=True)
                fig_j = create_chart(df_jeonse, selected_region, selected_date, "#000080")
                if fig_j:
                    st.markdown('<div class="static-chart">', unsafe_allow_html=True)
                    st.plotly_chart(fig_j, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("데이터가 존재하지 않는 지역입니다.")
        else:
            st.info("날짜와 지역을 선택해 주세요.")

    except Exception as e:
        st.error(f"앱 실행 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
