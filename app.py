import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="Dr.J의 부동산", layout="centered")

# 2. 고도화된 디자인 커스텀 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Noto+Sans+KR', sans-serif;
    }

    .title-container {
        padding: 30px 0 10px 0;
        text-align: center;
        width: 100%;
    }
    
    .main-title {
        font-size: clamp(22px, 6vw, 30px);
        font-weight: 700;
        white-space: nowrap;
        letter-spacing: -1.5px;
        display: inline-block;
    }
    
    .brand-name {
        color: #006400; /* 짙은 그린 */
    }

    .selected-region-text {
        color: #DB7093; /* 짙은 핑크 */
        font-weight: 700;
    }

    /* 카드 디자인 */
    .metric-container {
        background-color: white;
        padding: 18px;
        border-radius: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        text-align: center;
    }
    
    .metric-label {
        font-size: 14px;
        color: #888;
        margin-bottom: 5px;
    }
    
    .metric-value {
        font-size: 26px;
        font-weight: 700;
    }

    header {visibility: hidden;}
    .block-container { padding-top: 1rem !important; }
    
    /* 그래프 섹션 타이틀 */
    .chart-title {
        font-size: 16px;
        font-weight: 700;
        margin: 25px 0 10px 0;
        color: #444;
    }
    </style>
    
    <div class="title-container">
        <div class="main-title">
            <span class="brand-name">Dr.J</span>의 부동산
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
    
    # 날짜 데이터 정렬 (그래프를 위해)
    df_m['날짜'] = df_m['날짜'].astype(str)
    df_j['날짜'] = df_j['날짜'].astype(str)
    return df_m, df_j

def create_chart(df, region, date, color):
    # 선택된 날짜 포함 최근 4개 데이터 추출
    idx = df[df['날짜'] == date].index[0]
    start_idx = max(0, idx - 3)
    recent_df = df.iloc[start_idx : idx + 1]
    
    fig = px.line(recent_df, x='날짜', y=region, markers=True)
    fig.update_traces(line_color=color, line_width=3, marker=dict(size=8))
    fig.update_layout(
        height=200,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, title=""),
        yaxis=dict(showgrid=True, gridcolor='#eee', title=""),
        hovermode="x unified"
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
            selected_region = st.selectbox("🔍 지역 검색 및 선택", options=["지역을 입력하세요"] + region_list)

        if selected_region != "지역을 입력하세요":
            m_val = df_maemae.loc[df_maemae['날짜'] == selected_date, selected_region].values[0]
            j_val = df_jeonse.loc[df_jeonse['날짜'] == selected_date, selected_region].values[0]

            st.markdown(f"#### 📍 <span class='selected-region-text'>{selected_region}</span> 시황", unsafe_allow_html=True)
            
            # 1. 수치 카드
            c1, c2 = st.columns(2)
            m_color = "#e74c3c" if m_val > 0 else "#000080" if m_val < 0 else "#333"
            j_color = "#e74c3c" if j_val > 0 else "#000080" if j_val < 0 else "#333"

            with c1:
                st.markdown(f'<div class="metric-container"><div class="metric-label">매매 증감</div><div class="metric-value" style="color: {m_color};">{m_val:+.2f}%</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="metric-container"><div class="metric-label">전세 증감</div><div class="metric-value" style="color: {j_color};">{j_val:+.2f}%</div></div>', unsafe_allow_html=True)

            # 2. 그래프 영역 (4주 트렌드)
            st.markdown('<div class="chart-title">📈 최근 4주 매매 흐름</div>', unsafe_allow_html=True)
            st.plotly_chart(create_chart(df_maemae, selected_region, selected_date, "#e74c3c"), use_container_width=True, config={'displayModeBar': False})

            st.markdown('<div class="chart-title">📈 최근 4주 전세 흐름</div>', unsafe_allow_html=True)
            st.plotly_chart(create_chart(df_jeonse, selected_region, selected_date, "#000080"), use_container_width=True, config={'displayModeBar': False})

        else:
            st.info("조회할 지역명을 입력하거나 선택해 주세요.")

    except Exception as e:
        st.error(f"데이터 처리 오류: {e}")

if __name__ == "__main__":
    main()
