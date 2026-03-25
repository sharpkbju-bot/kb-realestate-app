import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정 (앱 설치 이름 및 아이콘)
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
        color: #FF4500; /* 진한 주황색 */
        font-size: clamp(20px, 6vw, 30px);
        font-weight: 900;
    }

    /* 순위 카드 디자인 */
    .rank-card {
        background-color: #fffaf0;
        padding: 12px 15px;
        border-radius: 12px;
        margin-bottom: 8px;
        border-left: 5px solid #FF4500;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .rank-num { font-weight: 900; color: #FF4500; font-size: 1.1em; width: 30px; }
    .rank-name { font-weight: 700; color: #333; flex-grow: 1; }
    .rank-val { font-weight: 900; color: #e74c3c; }

    /* 수치 카드 디자인 */
    .metric-container {
        background-color: white;
        padding: 22px;
        border-radius: 18px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.06);
        border: 1px solid #f0f0f0;
        text-align: center;
        margin-bottom: 15px;
    }
    
    .metric-label { font-size: 15px; color: #4B0082; font-weight: 800; margin-bottom: 8px; }
    .metric-value { font-size: 30px; font-weight: 700; }

    /* 그래프 섹션 타이틀 */
    .chart-title {
        font-size: 18px;
        font-weight: 800;
        margin: 40px 0 15px 0;
        color: #C71585; /* 진한 핑크 */
        border-left: 6px solid #C71585;
        padding-left: 14px;
    }

    /* 컬럼 간격 조절 */
    [data-testid="column"] { padding: 0 10px !important; }

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
    
    # 날짜 컬럼을 제외한 모든 컬럼을 숫자형으로 변환 (에러 발생 시 NaN 처리)
    cols_to_convert = [c for c in df_m.columns if c != '날짜']
    df_m[cols_to_convert] = df_m[cols_to_convert].apply(pd.to_numeric, errors='coerce').fillna(0)
    df_j[cols_to_convert] = df_j[cols_to_convert].apply(pd.to_numeric, errors='coerce').fillna(0)
    
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
        
        # 상단 입력 컨트롤
        col_date, col_search = st.columns([1, 1.5])
        with col_date:
            date_list = df_maemae['날짜'].unique().tolist()
            selected_date = st.selectbox("📅 날짜 선택", date_list, index=len(date_list)-1)

        region_list = [col for col in df_maemae.columns if col != '날짜']
        with col_search:
            selected_region = st.selectbox("🔍 지역 검색 및 선택", options=["지역을 입력하세요."] + region_list)

        # --- 🔥 TOP 10 상승 지역 섹션 ---
        st.markdown(f'<div class="chart-title">🔥 {selected_date} 주간 매매 상승 TOP 10</div>', unsafe_allow_html=True)
        
        # 해당 날짜 행 추출
        current_row = df_maemae[df_maemae['날짜'] == selected_date].drop(columns=['날짜']).iloc[0]
        
        # 숫자형 데이터임을 보장한 뒤 정렬 (오류 해결 포인트)
        top_10 = current_row[current_row > 0].sort_values(ascending=False).head(10)

        if not top_10.empty:
            for i, (name, val) in enumerate(top_10.items()):
                st.markdown(f"""
                    <div class="rank-card">
                        <span class="rank-num">{i+1}</span>
                        <span class="rank-name">{name}</span>
                        <span class="rank-val">+{val:.2f}%</span>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("상승한 지역이 없습니다.")

        st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)

        # --- 📍 상세 시황 섹션 ---
        if selected_region != "지역을 입력하세요.":
            if selected_region in df_maemae.columns:
                m_val = df_maemae.loc[df_maemae['날짜'] == selected_date, selected_region].values[0]
                j_val = df_jeonse.loc[df_jeonse['날짜'] == selected_date, selected_region].values[0]

                st.markdown(f"#### 📍 <span style='color:#DB7093; font-weight:700;'>{selected_region}</span> 상세 시황", unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                m_color = "#e74c3c" if m_val > 0 else "#000080" if m_val < 0 else "#333"
                j_color = "#e74c3c" if j_val > 0 else "#000080" if j_val < 0 else "#333"

                with c1:
                    st.markdown(f'<div class="metric-container"><div class="metric-label">전주 대비 매매 증감</div><div class="metric-value" style="color: {m_color};">{m_val:+.2f}%</div></div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div class="metric-container"><div class="metric-label">전주 대비 전세 증감</div><div class="metric-value" style="color: {j_color};">{j_val:+.2f}%</div></div>', unsafe_allow_html=True)

                st.markdown('<div class="chart-title">📈 매매 지수 트렌드 (4주)</div>', unsafe_allow_html=True)
                fig_m = create_chart(df_maemae, selected_region, selected_date, "#e74c3c")
                if fig_m:
                    st.markdown('<div class="static-chart">', unsafe_allow_html=True)
                    st.plotly_chart(fig_m, use_container_width=True, config={'staticPlot': True})
                    st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="chart-title">📉 전세 지수 트렌드 (4주)</div>', unsafe_allow_html=True)
                fig_j = create_chart(df_jeonse, selected_region, selected_date, "#000080")
                if fig_j:
                    st.markdown('<div class="static-chart">', unsafe_allow_html=True)
                    st.plotly_chart(fig_j, use_container_width=True, config={'staticPlot': True})
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("상세 분석을 원하시면 지역을 선택해 주세요.")

    except Exception as e:
        st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
